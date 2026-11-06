"""Offline contract tests; run python -m unittest quality_guardian/test_niftyvid_wan_adapter.py."""
import unittest
try:
    from quality_guardian.niftyvid_wan_adapter import make_payload, parse_complete_sse
except ImportError:
    from niftyvid_wan_adapter import make_payload, parse_complete_sse

class NiftyVidContractTests(unittest.TestCase):
    def test_sixteen_inputs(self):
        data = make_payload("/tmp/gradio/heroine.png")["data"]
        self.assertEqual(len(data), 16)
        self.assertEqual(data[5], 3.5)
        self.assertEqual(data[11], "UniPCMultistep")
    def test_caps(self):
        with self.assertRaises(ValueError):
            make_payload("x", duration=5)
        with self.assertRaises(ValueError):
            make_payload("x", steps=13)
    def test_sse_completion(self):
        self.assertEqual(parse_complete_sse([
            "event: generating\n", "data: []\n", "\n",
            "event: complete\n", 'data: [{"url":"https://example.org/a.mp4"}]\n', "\n"
        ]), "https://example.org/a.mp4")
    def test_missing_video(self):
        with self.assertRaises(ValueError):
            parse_complete_sse(["event: complete\n", "data: [{}]\n", "\n"])
    def test_error(self):
        with self.assertRaises(RuntimeError):
            parse_complete_sse(["event: error\n", "data: queue full\n", "\n"])

if __name__ == "__main__":
    unittest.main()
