from decimal import Decimal, ROUND_HALF_UP


COMPONENTS = ("attendance", "midterm", "final")


def grade(weights, scores):
    """Return a two-decimal grade; reject unknown/missing inputs and invalid rules."""
    if set(weights) != set(COMPONENTS) or set(scores) != set(COMPONENTS):
        raise ValueError("components must be attendance, midterm, final")
    w = {name: Decimal(str(weights[name])) for name in COMPONENTS}
    s = {name: Decimal(str(scores[name])) for name in COMPONENTS}
    if any(not x.is_finite() or x < 0 for x in w.values()) or sum(w.values()) != 100:
        raise ValueError("weights must be nonnegative and sum to 100")
    if any(not x.is_finite() or x < 0 or x > 100 for x in s.values()):
        raise ValueError("scores must be between 0 and 100")
    return str((sum(w[k] * s[k] for k in COMPONENTS) / 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
