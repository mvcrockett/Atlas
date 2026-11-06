"""Offline contract tests for execution_bridge; no external services."""
import tempfile
import unittest
from pathlib import Path
try:
    from quality_guardian.execution_bridge import ExecutionBridge, BridgeError, Policy
except ImportError:
    from execution_bridge import ExecutionBridge, BridgeError, Policy

MP4 = (b"\x00\x00\x00\x10ftypisom\x00\x00\x00\x00"
       b"\x00\x00\x00\x08moov")

class FakeTransport:
    is_mock = True
    def __init__(self, states=None, video=MP4, failures=0):
        self.states = iter(states or [{"state": "queued"}, {"state": "complete", "url": "https://example.org/movie.mp4"}])
        self.video = video
        self.failures = failures
        self.uploads = 0
    def upload(self, data, filename, timeout):
        self.uploads += 1
        if self.failures:
            self.failures -= 1
            raise TimeoutError("mock transient failure")
        return "/tmp/gradio/heroine.png"
    def submit(self, payload, timeout):
        assert len(payload["data"]) == 16
        return "mock-job-123"
    def status(self, job_id, timeout):
        return next(self.states)
    def download(self, url, max_bytes, timeout):
        return self.video

def payload(path, filename):
    return {"data": [path] * 16}

class BridgeTests(unittest.TestCase):
    def run_fake(self, fake=None, policy=None):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder) / "clip.mp4"
            result = ExecutionBridge(fake or FakeTransport(), policy).run(b"fake-image", "heroine.png", payload, out)
            self.assertTrue(out.is_file())
            self.assertEqual(out.read_bytes(), MP4)
            return result

    def test_success_with_polling_and_mp4(self):
        result = self.run_fake()
        self.assertEqual(result["paid_usd"], 0)
        self.assertTrue(result["mock"])
        self.assertEqual(result["job_id"], "mock-job-123")
        self.assertEqual([entry["event"] for entry in result["audit"]],
                         ["started", "uploaded", "submitted", "polled", "saved"])

    def test_retry_then_success(self):
        fake = FakeTransport(failures=1)
        self.run_fake(fake)
        self.assertEqual(fake.uploads, 2)

    def test_retry_exhaustion(self):
        with self.assertRaisesRegex(BridgeError, "Retry limit"):
            self.run_fake(FakeTransport(failures=3))

    def test_policy_rejects_live_and_paid(self):
        for policy in (Policy(mock_only=False), Policy(max_spend_usd=0.01)):
            with self.assertRaisesRegex(BridgeError, "FAIL CLOSED"):
                ExecutionBridge(FakeTransport(), policy)

    def test_non_mock_transport_rejected(self):
        fake = FakeTransport()
        fake.is_mock = False
        with self.assertRaisesRegex(BridgeError, "FAIL CLOSED"):
            ExecutionBridge(fake)

    def test_polling_limit(self):
        with self.assertRaisesRegex(BridgeError, "Polling limit"):
            self.run_fake(FakeTransport(states=[{"state": "running"}] * 10), Policy(max_polls=2))

    def test_failed_job(self):
        with self.assertRaisesRegex(BridgeError, "Job failed"):
            self.run_fake(FakeTransport(states=[{"state": "failed"}]))

    def test_untrusted_url(self):
        with self.assertRaisesRegex(BridgeError, "HTTPS"):
            self.run_fake(FakeTransport(states=[{"state": "complete", "url": "http://example.org/movie.mp4"}]))

    def test_invalid_mp4(self):
        with self.assertRaisesRegex(BridgeError, "Invalid, oversized"):
            self.run_fake(FakeTransport(video=b"not mp4"))

    def test_size_limits(self):
        with self.assertRaisesRegex(BridgeError, "Input image"):
            ExecutionBridge(FakeTransport(), Policy(max_input_bytes=2)).run(b"abc", "a.png", payload, "x.mp4")
        with self.assertRaisesRegex(BridgeError, "Invalid, oversized"):
            self.run_fake(FakeTransport(), Policy(max_output_bytes=16))

    def test_host_allowlist(self):
        with self.assertRaisesRegex(BridgeError, "allowlisted"):
            self.run_fake(FakeTransport(states=[{"state": "complete", "url": "https://evil.example/movie.mp4"}]))
        with self.assertRaisesRegex(BridgeError, "allowlisted"):
            self.run_fake(FakeTransport(states=[{"state": "complete", "url": "https://example.org:444/movie.mp4"}]))

    def test_ip_literal_rejected(self):
        with self.assertRaisesRegex(BridgeError, "IP literals"):
            self.run_fake(FakeTransport(states=[{"state": "complete", "url": "https://127.0.0.1/movie.mp4"}]))

    def test_mp4_missing_moov(self):
        with self.assertRaisesRegex(BridgeError, "moov"):
            self.run_fake(FakeTransport(video=MP4[:16]))

    def test_mp4_corrupt_box(self):
        with self.assertRaisesRegex(BridgeError, "box size"):
            self.run_fake(FakeTransport(video=b"\\xff\\xff\\xff\\xffftyp" + MP4[8:]))

    def test_audit_does_not_leak_url_or_image(self):
        result = self.run_fake()
        serialized = str(result["audit"])
        self.assertNotIn("example.org", serialized)
        self.assertNotIn("fake-image", serialized)
        self.assertTrue(all(entry["paid_usd"] == 0.0 for entry in result["audit"]))

    def test_deadline(self):
        ticks = iter([0, 2])
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(BridgeError, "deadline"):
                ExecutionBridge(FakeTransport(), Policy(timeout_seconds=1), clock=lambda: next(ticks)).run(
                    b"img", "a.png", payload, Path(folder) / "x.mp4")

if __name__ == "__main__":
    unittest.main()
