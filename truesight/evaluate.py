"""Small CSV/JSON interface; no model loading, training, or threshold fitting."""

import argparse
import csv
import json
from math import isfinite
from pathlib import Path

from .reliability import evaluate


def evaluate_csv(path, *, decision_threshold, acceptance_threshold=None):
    """Require explicit provenance markers and keep failed rows in accounting."""
    for name, value in (("decision_threshold", decision_threshold),
                        ("acceptance_threshold", acceptance_threshold)):
        if name == "acceptance_threshold" and value is None:
            continue
        if isinstance(value, (str, bytes, bool)):
            raise ValueError(f"{name} must be finite")
        try:
            valid = isfinite(value)
        except (TypeError, OverflowError) as exc:
            raise ValueError(f"{name} must be finite") from exc
        if not valid:
            raise ValueError(f"{name} must be finite")
    with Path(path).open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"sample_id", "label", "detection_score", "confidence_score",
                    "status", "data_kind", "split", "evaluation_condition"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"required CSV columns: {sorted(required)}")
        rows = list(reader)
    if not rows:
        raise ValueError("CSV must contain rows")
    seen = set()
    for row in rows:
        key = row["sample_id"]
        if not key or key in seen:
            raise ValueError("sample_id must be nonempty and unique per detector run")
        seen.add(key)
        if row["label"] not in ("0", "1"):
            raise ValueError("label must be 0 or 1")
        if row["status"] not in ("ok", "error"):
            raise ValueError("status must be ok or error")
        if row["status"] == "error" and not row.get("error_reason"):
            raise ValueError("failed rows need error_reason")
        if row["status"] == "ok" and (not row["detection_score"] or not row["confidence_score"]):
            raise ValueError("successful rows need both scores")
        if row["data_kind"] not in ("simulated", "real_detector_output"):
            raise ValueError("explicit data_kind required")
        if row["split"] not in ("synthetic_test", "technical_trial", "development", "validation", "final_test"):
            raise ValueError("unknown split")
        if not row["evaluation_condition"]:
            raise ValueError("evaluation_condition required")
    kinds, splits = {r["data_kind"] for r in rows}, {r["split"] for r in rows}
    if len(kinds) != 1 or len(splits) != 1:
        raise ValueError("one data_kind and split per evaluation file")
    if ("simulated" in kinds) != ("synthetic_test" in splits):
        raise ValueError("simulations must use synthetic_test, and only simulations may use it")

    def summarize(subset):
        scored = [r for r in subset if r["status"] == "ok"]
        metrics = None
        if scored:
            metrics = evaluate([int(r["label"]) for r in scored],
                               [float(r["detection_score"]) for r in scored],
                               [float(r["confidence_score"]) for r in scored],
                               decision_threshold=decision_threshold,
                               acceptance_threshold=acceptance_threshold)
        total = len(subset)
        accepted = metrics["selective"]["accepted_count"] if metrics else 0
        return {"input_count": total, "scored_count": len(scored),
                "failure_count": total - len(scored),
                "scoring_coverage": len(scored) / total,
                "end_to_end_acceptance_coverage": accepted / total,
                "failed_real_count": sum(r["label"] == "0" and r["status"] == "error" for r in subset),
                "failed_generated_count": sum(r["label"] == "1" and r["status"] == "error" for r in subset),
                "metrics_on_scored_rows": metrics}

    return {"schema_version": "1.0", "data_kind": next(iter(kinds)),
            "split": next(iter(splits)),
            "decision_threshold": decision_threshold,
            "acceptance_threshold": acceptance_threshold,
            "overall": summarize(rows),
            "by_condition": {condition: summarize([r for r in rows if r["evaluation_condition"] == condition])
                             for condition in sorted({r["evaluation_condition"] for r in rows})}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_json", type=Path)
    parser.add_argument("--decision-threshold", type=float, required=True)
    parser.add_argument("--acceptance-threshold", type=float)
    args = parser.parse_args()
    if args.output_json.exists() or args.input_csv.resolve() == args.output_json.resolve():
        parser.error("output must be a new path; existing files are never overwritten")
    try:
        result = evaluate_csv(args.input_csv, decision_threshold=args.decision_threshold,
                              acceptance_threshold=args.acceptance_threshold)
        payload = json.dumps(result, indent=2, allow_nan=False) + "\n"
        with args.output_json.open("x", encoding="utf-8") as stream:
            stream.write(payload)
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Evaluation failed: {exc}\n")


if __name__ == "__main__":
    main()
