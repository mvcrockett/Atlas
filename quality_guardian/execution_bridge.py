"""Offline-only Gradio execution bridge. No HTTP client or live transport."""
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit
import hashlib
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

    def validate(self):
        if self.max_spend_usd != 0 or not self.mock_only:
            raise BridgeError("FAIL CLOSED: Sprint 1 permits only $0 mock execution")
        if self.timeout_seconds <= 0 or self.max_polls < 1 or self.max_retries < 0:
            raise BridgeError("Invalid execution bounds")
        if self.max_input_bytes < 1 or self.max_output_bytes < 12:
            raise BridgeError("Invalid size bounds")

def _https_url(url):
    if not isinstance(url, str):
        raise BridgeError("Missing HTTPS URL")
    p = urlsplit(url)
    if p.scheme != "https" or not p.hostname or p.username or p.password:
        raise BridgeError("Only credential-free HTTPS URLs permitted")
    if p.hostname == "localhost" or p.hostname.endswith(".local"):
        raise BridgeError("Local URLs prohibited")
    return url

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
        deadline = self.clock() + self.policy.timeout_seconds
        remote_path = self._bounded(lambda timeout: self.transport.upload(image_bytes, filename, timeout), deadline)
        if not isinstance(remote_path, str) or not remote_path.startswith("/tmp/"):
            raise BridgeError("Untrusted upload path")
        payload = payload_factory(remote_path, filename=filename)
        if not isinstance(payload, dict) or "data" not in payload:
            raise BridgeError("Invalid generated payload")
        job_id = self._bounded(lambda timeout: self.transport.submit(payload, timeout), deadline)
        if not isinstance(job_id, str) or not job_id or len(job_id) > 200:
            raise BridgeError("Invalid job identifier")
        video_url = None
        for _ in range(self.policy.max_polls):
            state = self._bounded(lambda timeout: self.transport.status(job_id, timeout), deadline)
            if not isinstance(state, dict):
                raise BridgeError("Invalid job status")
            if state.get("state") == "complete":
                video_url = _https_url(state.get("url"))
                break
            if state.get("state") in ("failed", "error", "cancelled"):
                raise BridgeError("Job failed: " + str(state.get("state")))
            if state.get("state") not in ("queued", "running"):
                raise BridgeError("Unknown job state")
            self.sleep(min(0.05, max(0, deadline - self.clock())))
        if not video_url:
            raise BridgeError("Polling limit reached without completion")
        content = self._bounded(lambda timeout: self.transport.download(video_url, self.policy.max_output_bytes + 1, timeout), deadline)
        if not isinstance(content, bytes) or len(content) > self.policy.max_output_bytes or len(content) < 12 or content[4:8] != b"ftyp":
            raise BridgeError("Invalid, oversized, or missing MP4")
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
        return {"job_id": job_id, "output_path": str(path), "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(), "mock": True, "paid_usd": 0.0}
