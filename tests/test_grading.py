import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "core"))
from grading import grade


class GradingTests(unittest.TestCase):
    def test_tenant_formulas_differ(self):
        scores = {"attendance": 100, "midterm": 80, "final": 70}
        self.assertEqual(grade({"attendance": 10, "midterm": 30, "final": 60}, scores), "76.00")
        self.assertEqual(grade({"attendance": 20, "midterm": 20, "final": 60}, scores), "78.00")

    def test_invalid_formula_rejected(self):
        with self.assertRaises(ValueError):
            grade({"attendance": 10, "midterm": 30, "final": 70}, {"attendance": 100, "midterm": 80, "final": 70})


if __name__ == "__main__":
    unittest.main()
