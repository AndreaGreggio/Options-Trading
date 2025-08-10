import math

SQRT_2PI = math.sqrt(2.0 * math.pi)


def norm_pdf(x: float) -> float:
    """Standard normal pdf φ(x)."""
    return math.exp(-0.5 * x * x) / SQRT_2PI


def norm_cdf(x: float) -> float:
    """Standard normal cdf N(x) using erf (no SciPy required)."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
