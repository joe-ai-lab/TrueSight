"""Synthetic unit tests only: no images, model scores, or detector claims."""

import csv
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from truesight.evaluate import evaluate_csv
from truesight.reliability import auroc, evaluate


class ReliabilityTests(unittest.TestCase):
    def score(self, labels, scores, confidence, **kwargs):
        return evaluate(labels, scores, confidence, decision_threshold=0.5, **kwargs)

    def test_perfect_predictions(self):
        r = self.score([0, 1, 0, 1], [.1, .9, .2, .8], [.9, .9, .8, .8])
        self.assertEqual(r["auroc"], 1)
        self.assertEqual(r["full"]["fpr"], 0)
        self.assertEqual(r["full"]["fnr"], 0)
        self.assertEqual(r["aurc"], 0)

    def test_high_confidence_errors_worsen_selection(self):
        r = self.score([0, 1, 0, 1], [.9, .1, .1, .9], [.99, .98, .7, .6],
                       acceptance_threshold=.95)
        self.assertEqual(r["full"]["risk"], .5)
        self.assertEqual(r["selective"]["risk"], 1)
        self.assertEqual(r["selective"]["coverage"], .5)
        self.assertAlmostEqual(r["aurc"], (1 + 1 + 2/3 + .5) / 4)
        good = self.score([0, 1, 0, 1], [.9, .1, .1, .9], [.6, .7, .98, .99])
        self.assertLess(good["aurc"], r["aurc"])

    def test_imbalanced_counts_and_class_coverage(self):
        r = self.score([0, 0, 0, 0, 1], [.1, .1, .1, .9, .1], [1, 1, 1, 0, 0],
                       acceptance_threshold=.5)
        self.assertEqual(r["full"]["fpr"], .25)
        self.assertEqual(r["full"]["fnr"], 1)
        self.assertEqual(r["selective"]["real_coverage"], .75)
        self.assertEqual(r["selective"]["generated_coverage"], 0)
        self.assertIsNone(r["selective"]["fnr"])

    def test_all_rejected_and_no_rejection(self):
        r = self.score([0, 1], [.1, .9], [.2, .3], acceptance_threshold=1)
        self.assertEqual(r["selective"]["coverage"], 0)
        self.assertIsNone(r["selective"]["risk"])
        self.assertIsNone(r["selective"]["fpr"])
        self.assertEqual(r["auroc"], 1)
        self.assertEqual(r["aurc"], 0)  # ranking metrics use all scored rows
        self.assertEqual(self.score([0, 1], [.1, .9], [.2, .3])["selective"]["coverage"], 1)

    def test_single_class_and_single_sample(self):
        r = self.score([0], [.9], [.8])
        self.assertIsNone(r["auroc"])
        self.assertIsNone(r["full"]["fnr"])
        self.assertEqual(r["full"]["fpr"], 1)
        self.assertEqual(r["aurc"], 1)

    def test_threshold_boundaries_and_unbounded_scores(self):
        r = self.score([0, 1], [.5, .5], [.5, .5], acceptance_threshold=.5)
        self.assertEqual(r["full"]["tn"], 1)
        self.assertEqual(r["full"]["fn"], 1)
        self.assertEqual(r["selective"]["coverage"], 1)
        self.assertEqual(auroc([0, 1], [-100, 100]), 1)

    def test_auroc_against_pairwise_oracle(self):
        labels = [0, 1, 0, 1, 1]
        for scores in itertools.product([0, 1, 2], repeat=len(labels)):
            pos = [s for y, s in zip(labels, scores) if y]
            neg = [s for y, s in zip(labels, scores) if not y]
            expected = sum((p > n) + .5 * (p == n) for p in pos for n in neg) / (len(pos) * len(neg))
            self.assertAlmostEqual(auroc(labels, scores), expected)

    def test_tie_aurc_against_exhaustive_permutations(self):
        # One high-confidence correct sample, then a tied group with two errors.
        labels, scores = [0, 0, 1, 1], [.1, .9, .1, .9]
        r = self.score(labels, scores, [1, .5, .5, .5])
        expected = []
        for errors in itertools.permutations([1, 1, 0]):
            sequence = [0, *errors]
            expected.append(sum(sum(sequence[:k]) / k for k in range(1, 5)) / 4)
        self.assertAlmostEqual(r["aurc"], sum(expected) / len(expected))
        self.assertEqual([p["coverage"] for p in r["risk_coverage"]], [0, .25, 1])
        reverse = self.score(labels[::-1], scores[::-1], [.5, .5, .5, 1])
        self.assertEqual(r["aurc"], reverse["aurc"])
        tied = self.score([0, 1], [.9, .9], [1, 1])
        self.assertEqual(tied["aurc"], .5)

    def test_invalid_inputs(self):
        cases = [([], [], []), ([2], [.2], [.3]), ([0], [], [.3]),
                 ([0], [float("nan")], [.3]), ([0], [.2], [float("inf")]),
                 ([0], ["0.1"], [.3])]
        for args in cases:
            with self.subTest(args=args), self.assertRaises(ValueError):
                self.score(*args)
        with self.assertRaises(ValueError):
            evaluate([0], [.1], [.2], decision_threshold=float("nan"))


class CsvTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "simulated.csv"
        self.rows = [dict(sample_id="s1", label="0", detection_score=".1", confidence_score=".8",
                          status="ok", data_kind="simulated", split="synthetic_test",
                          evaluation_condition="synthetic", error_reason=""),
                     dict(sample_id="s2", label="1", detection_score="", confidence_score="",
                          status="error", data_kind="simulated", split="synthetic_test",
                          evaluation_condition="synthetic", error_reason="simulated failure")]

    def write(self):
        with self.path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.rows[0].keys())
            writer.writeheader()
            writer.writerows(self.rows)

    def run_eval(self):
        self.write()
        return evaluate_csv(self.path, decision_threshold=.5)

    def test_failures_are_accounted_for(self):
        r = self.run_eval()["overall"]
        self.assertEqual(r["failure_count"], 1)
        self.assertEqual(r["end_to_end_acceptance_coverage"], .5)
        self.assertEqual(r["failed_generated_count"], 1)
        self.assertIsNone(r["metrics_on_scored_rows"]["auroc"])

    def test_all_failed(self):
        self.rows[0].update(status="error", error_reason="simulated failure")
        r = self.run_eval()["overall"]
        self.assertIsNone(r["metrics_on_scored_rows"])
        self.assertEqual(r["scoring_coverage"], 0)

    def test_missing_scores_and_invalid_threshold_even_if_all_failed(self):
        self.rows[0]["confidence_score"] = ""
        with self.assertRaises(ValueError):
            self.run_eval()
        self.rows[0].update(status="error", error_reason="simulated failure")
        self.write()
        with self.assertRaises(ValueError):
            evaluate_csv(self.path, decision_threshold=float("inf"))

    def test_conditions_are_separate(self):
        self.rows[1]["evaluation_condition"] = "failed_condition"
        r = self.run_eval()
        self.assertEqual(r["by_condition"]["synthetic"]["scored_count"], 1)
        self.assertIsNone(r["by_condition"]["failed_condition"]["metrics_on_scored_rows"])

    def test_duplicate_mixed_split_and_simulation_markers(self):
        for field, value in [("sample_id", "s1"), ("split", "final_test"),
                             ("data_kind", "real_detector_output"), ("status", "missing")]:
            old = self.rows[1][field]
            self.rows[1][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.run_eval()
            self.rows[1][field] = old

    def test_cli_and_overwrite_protection(self):
        self.write()
        output = Path(self.temp.name) / "summary.json"
        command = [sys.executable, "-m", "truesight.evaluate", str(self.path), str(output),
                   "--decision-threshold", "0.5"]
        run = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        payload = output.read_bytes()
        self.assertEqual(json.loads(payload)["data_kind"], "simulated")
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
        self.assertEqual(output.read_bytes(), payload)


if __name__ == "__main__":
    unittest.main()
