"""Offline-only Gradio execution bridge. No HTTP client or live transport."""
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit
import hashlib
import ipaddress
import json
import struct
import time

class BridgeError(RuntimeError):
    pass

@dataclass(frozen=True)
class Policy:
    mock_only: bool = True
    max_spend_usd: float = 0.0
    timeout_seconds: float = 30.0
    max_polls: int = 5
    max_retries: int = 1
    max_input_bytes: int = 10_000_000
    max_output_bytes: int = 30_000_000
    allowed_output_hosts: tuple = ("example.org",)

    def validate(self):
        if self.max_spend_usd != 0 or not self.mock_only:
            raise BridgeError("FAIL CLOSED: Sprint 1 permits only $0 mock execution")
        if self.timeout_seconds <= 0 or self.max_polls < 1 or self.max_retries < 0:
            raise BridgeError("Invalid execution bounds")
        if not self.allowed_output_hosts or any(not isinstance(h, str) or not h or h != h.lower() or h.endswith('.') or '/' in h for h in self.allowed_output_hosts):
            raise BridgeError("Invalid output-host allowlist")
        if self.max_input_bytes < 1 or self.max_output_bytes < 16:
            raise BridgeError("Invalid size bounds")

def _https_url(url, allowed_hosts):
    if not isinstance(url, str):
        raise BridgeError("Missing HTTPS URL")
    try:
        p = urlsplit(url)
        host = p.hostname
        if p.scheme != "https" or not host or p.username or p.password or p.fragment:
            raise ValueError("Invalid URL")
        port = p.port
        ipaddress.ip_address(host)
        raise ValueError("IP literals are prohibited")
    except ValueError as exc:
        if "IP literals" in str(exc):
            raise BridgeError("IP literals are prohibited") from exc
        if not isinstance(url, str) or "://" not in url:
            raise BridgeError("Only credential-free HTTPS URLs permitted") from exc
        # Ordinary DNS hostnames are not IP literals.
        try:
            p = urlsplit(url)
            host = p.hostname
            port = p.port
        except ValueError as err:
            raise BridgeError("Invalid video URL") from err
        if p.scheme != "https" or not host or p.username or p.password or p.fragment:
            raise BridgeError("Only credential-free HTTPS URLs permitted") from exc
    if port not in (None, 443) or host not in allowed_hosts:
        raise BridgeError("Video host not allowlisted")
    return url


def _validate_mp4(content):
    """Parse top-level ISO BMFF boxes; require ftyp and movie metadata (moov)."""
    if not isinstance(content, bytes) or len(content) < 24:
        raise BridgeError("Invalid, oversized, or missing MP4")
    pos = 0
    boxes = []
    while pos < len(content):
        if len(content) - pos < 8:
            raise BridgeError("Truncated MP4 box header")
        size, typ = struct.unpack_from(">I4s", content, pos)
        header = 8
        if size == 1:
            if len(content) - pos < 16:
                raise BridgeError("Truncated extended MP4 box")
            size = struct.unpack_from(">Q", content, pos + 8)[0]
            header = 16
        elif size == 0:
            size = len(content) - pos
        if size < header or size > len(content) - pos:
            raise BridgeError("Invalid MP4 box size")
        boxes.append(typ)
        pos += size
    if boxes[0] != b"ftyp" or b"moov" not in boxes:
        raise BridgeError("MP4 requires ftyp and moov boxes")
    return True

class ExecutionBridge:
    """Transport is injected, explicitly mocked, and never instantiated here."""
    def __init__(self, transport, policy=None, clock=None, sleeper=None):
        self.policy = policy or Policy()
        self.policy.validate()
        if not getattr(transport, "is_mock", False):
            raise BridgeError("FAIL CLOSED: transport must be explicitly marked mock")
        self.transport = transport
        self.clock = clock or time.monotonic
        self.sleep = sleeper or time.sleep
        self.audit = []

    def _record(self, event, **fields):
        self.audit.append({"event": event, "mock": True, "paid_usd": 0.0, **fields})

    def _bounded(self, operation, deadline):
        for attempt in range(self.policy.max_retries + 1):
            if self.clock() >= deadline:
                raise BridgeError("Overall deadline exceeded")
            try:
                return operation(timeout=max(0.001, deadline - self.clock()))
            except (TimeoutError, ConnectionError) as exc:
                if attempt >= self.policy.max_retries:
                    raise BridgeError("Retry limit exceeded") from exc
                self.sleep(min(0.05, max(0, deadline - self.clock())))

    def run(self, image_bytes, filename, payload_factory, output_path):
        """Mock upload -> submit -> poll -> download -> validate -> atomic MP4 save."""
        if not isinstance(image_bytes, bytes) or not (0 < len(image_bytes) <= self.policy.max_input_bytes):
            raise BridgeError("Input image exceeds bounds or is empty")
        if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            raise BridgeError("Unsupported input image extension")
        self.audit = []
        self._record("started", input_bytes=len(image_bytes))
        deadline = self.clock() + self.policy.timeout_seconds
        remote_path = self._bounded(lambda timeout: self.transport.upload(image_bytes, filename, timeout), deadline)
        if not isinstance(remote_path, str) or not remote_path.startswith("/tmp/"):
            raise BridgeError("Untrusted upload path")
        self._record("uploaded")
        payload = payload_factory(remote_path, filename=filename)
        if not isinstance(payload, dict) or "data" not in payload:
            raise BridgeError("Invalid generated payload")
        job_id = self._bounded(lambda timeout: self.transport.submit(payload, timeout), deadline)
        if not isinstance(job_id, str) or not job_id or len(job_id) > 200:
            raise BridgeError("Invalid job identifier")
        self._record("submitted", job_id=job_id)
        video_url = None
        for _ in range(self.policy.max_polls):
            state = self._bounded(lambda timeout: self.transport.status(job_id, timeout), deadline)
            if not isinstance(state, dict):
                raise BridgeError("Invalid job status")
            if state.get("state") == "complete":
                video_url = _https_url(state.get("url"), self.policy.allowed_output_hosts)
                break
            if state.get("state") in ("failed", "error", "cancelled"):
                raise BridgeError("Job failed: " + str(state.get("state")))
            self._record("polled", state=state.get("state"))
            if state.get("state") not in ("queued", "running"):
                raise BridgeError("Unknown job state")
            self.sleep(min(0.05, max(0, deadline - self.clock())))
        if not video_url:
            raise BridgeError("Polling limit reached without completion")
        content = self._bounded(lambda timeout: self.transport.download(video_url, self.policy.max_output_bytes + 1, timeout), deadline)
        if not isinstance(content, bytes) or len(content) > self.policy.max_output_bytes:
            raise BridgeError("Invalid, oversized, or missing MP4")
        _validate_mp4(content)
        path = Path(output_path)
        if path.suffix.lower() != ".mp4":
            raise BridgeError("Output must be .mp4")
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_suffix(".mp4.part")
        try:
            temp.write_bytes(content)
            temp.replace(path)
        finally:
            temp.unlink(missing_ok=True)
        self._record("saved", bytes=len(content), sha256=hashlib.sha256(content).hexdigest())
        return {"audit": list(self.audit), "job_id": job_id, "output_path": str(path), "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(), "mock": True, "paid_usd": 0.0}
