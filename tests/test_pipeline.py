import tempfile
import unittest
from pathlib import Path

from src.main import DEFAULT_INPUT, run_quality


class QualityPipelineTests(unittest.TestCase):
    def test_invalid_rows_are_quarantined_with_reason_counts(self):
        with tempfile.TemporaryDirectory() as directory:
            metrics = run_quality(DEFAULT_INPUT, Path(directory))
        self.assertEqual(metrics["input_rows"], 5)
        self.assertEqual(metrics["accepted_rows"], 2)
        self.assertEqual(metrics["duplicate"], 1)
        self.assertEqual(metrics["missing_required"], 1)
        self.assertEqual(metrics["negative_amount"], 1)


if __name__ == "__main__":
    unittest.main()
