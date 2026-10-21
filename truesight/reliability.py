"""Binary detection and selective-risk metrics using only the standard library.

Labels: real=0, generated=1. Detection scores increase toward generated;
confidence increases toward acceptance, regardless of predicted class.
"""

from collections import defaultdict
from math import isfinite


def _finite(values, name):
    result = []
    for value in values:
        if isinstance(value, (bool, str, bytes)):
            raise ValueError(f"{name} must contain finite numbers")
        try:
            number = float(value)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(f"{name} must contain finite numbers") from exc
        if not isfinite(number):
            raise ValueError(f"{name} must contain finite numbers")
        result.append(number)
    return result


def _rate(numerator, denominator):
    return numerator / denominator if denominator else None


def auroc(labels, scores):
    """Rank AUROC with half credit for ties; None when either class is absent."""
    labels = list(labels)
    scores = _finite(scores, "scores")
    if len(labels) != len(scores) or any(y not in (0, 1) for y in labels):
        raise ValueError("labels must be binary and match scores")
    positives = sum(labels)
    negatives = len(labels) - positives
    if not positives or not negatives:
        return None
    groups = defaultdict(lambda: [0, 0])
    for y, score in zip(labels, scores):
        groups[score][int(y)] += 1
    negative_below = 0
    wins = 0.0
    for score in sorted(groups):
        real, fake = groups[score]
        wins += fake * (negative_below + real / 2)
        negative_below += real
    return wins / (positives * negatives)


def _confusion(labels, predictions):
    tp = sum(y == 1 and p == 1 for y, p in zip(labels, predictions))
    fp = sum(y == 0 and p == 1 for y, p in zip(labels, predictions))
    tn = sum(y == 0 and p == 0 for y, p in zip(labels, predictions))
    fn = sum(y == 1 and p == 0 for y, p in zip(labels, predictions))
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn,
            "fpr": _rate(fp, fp + tn), "fnr": _rate(fn, fn + tp),
            "risk": _rate(fp + fn, len(labels))}


def evaluate(labels, detection_scores, confidence_scores, *,
             decision_threshold, acceptance_threshold=None):
    """Evaluate supplied scores without fitting thresholds or confidence rules.

    Prediction is detection_score > decision_threshold. Acceptance is confidence
    >= acceptance_threshold; None accepts all. RC thresholds include complete
    confidence tie groups. AURC is mean prefix risk, expected over uniformly
    random order within ties, computed analytically (no random sampling).
    Empty inputs are rejected. This function does not enforce dataset isolation.
    """
    labels = list(labels)
    scores = _finite(detection_scores, "detection_scores")
    confidence = _finite(confidence_scores, "confidence_scores")
    if not labels or len(labels) != len(scores) or len(labels) != len(confidence):
        raise ValueError("nonempty inputs must have equal lengths")
    if any(y not in (0, 1) for y in labels):
        raise ValueError("labels must be 0 (real) or 1 (generated)")
    threshold = _finite([decision_threshold], "decision_threshold")[0]
    accept_at = (None if acceptance_threshold is None else
                 _finite([acceptance_threshold], "acceptance_threshold")[0])
    predictions = [int(s > threshold) for s in scores]
    errors = [int(y != p) for y, p in zip(labels, predictions)]
    accepted = [accept_at is None or c >= accept_at for c in confidence]
    groups = defaultdict(list)
    for c, error in zip(confidence, errors):
        groups[c].append(error)
    n = len(labels)
    curve = [{"confidence_threshold": None, "accepted_count": 0,
              "coverage": 0.0, "risk": None}]
    count = cumulative_errors = 0
    area = 0.0
    for c in sorted(groups, reverse=True):
        size, group_errors = len(groups[c]), sum(groups[c])
        for j in range(1, size + 1):
            area += (cumulative_errors + j * group_errors / size) / (count + j)
        count += size
        cumulative_errors += group_errors
        curve.append({"confidence_threshold": c, "accepted_count": count,
                      "coverage": count / n, "risk": cumulative_errors / count})
    kept_y = [y for y, keep in zip(labels, accepted) if keep]
    kept_p = [p for p, keep in zip(predictions, accepted) if keep]
    full = _confusion(labels, predictions)
    selective = _confusion(kept_y, kept_p)
    selective.update({
        "accepted_count": sum(accepted), "rejected_count": n - sum(accepted),
        "coverage": sum(accepted) / n,
        "real_coverage": _rate(sum(keep for y, keep in zip(labels, accepted) if y == 0), labels.count(0)),
        "generated_coverage": _rate(sum(keep for y, keep in zip(labels, accepted) if y == 1), labels.count(1)),
        "rejected_risk": _rate(sum(e for e, keep in zip(errors, accepted) if not keep), n - sum(accepted)),
    })
    return {"sample_count": n, "real_count": labels.count(0),
            "generated_count": labels.count(1), "auroc": auroc(labels, scores),
            "decision_threshold": threshold, "acceptance_threshold": accept_at,
            "full": full, "selective": selective, "aurc": area / n,
            "aurc_convention": "mean_prefix_risk_expected_random_ties_v1",
            "risk_coverage": curve}
