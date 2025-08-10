from __future__ import annotations
from typing import Callable, Tuple
from .models import OptionSpec, MarketData, OptionType
from .black_scholes import bs_price


def implied_volatility(
    opt: OptionSpec,
    mkt: MarketData,
    target_price: float,
    bracket: Tuple[float, float] = (1e-6, 5.0),
    tol: float = 1e-8,
    max_iter: int = 100,
) -> float:
    """
    Find sigma such that BS price matches target_price using bisection.
    - bracket: search interval for sigma in vols (e.g., 0%..500%).
    Returns sigma as a decimal (e.g., 0.2 for 20%).
    """
    low, high = bracket
    if target_price <= 0:
        raise ValueError("target_price must be > 0")

    # Helper to price with a trial sigma
    def price_at(sigma: float) -> float:
        md = mkt.__class__(**{**mkt.__dict__, "volatility": sigma})
        return bs_price(opt, md)

    p_low, p_high = price_at(low), price_at(high)
    # Ensure the target is bracketed
    if not (p_low <= target_price <= p_high):
        # For puts that are deep ITM, the price decreases with sigma initially,
        # but the range [1e-6, 5.0] is usually sufficient. If not, raise.
        raise ValueError(
            "Target price not bracketed by (low, high). Try widening the bracket."
        )

    for _ in range(max_iter):
        mid = 0.5 * (low + high)
        p_mid = price_at(mid)
        if abs(p_mid - target_price) < tol:
            return mid
        if p_mid < target_price:
            low = mid
        else:
            high = mid
    return 0.5 * (low + high)
