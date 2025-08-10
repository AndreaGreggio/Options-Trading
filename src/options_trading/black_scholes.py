from __future__ import annotations
import math
from .models import OptionSpec, MarketData, OptionType
from .stats import norm_cdf


def _check_inputs(S: float, K: float, T: float, sigma: float) -> None:
    if S <= 0 or K <= 0:
        raise ValueError("S and K must be > 0")
    if T <= 0:
        raise ValueError("T must be > 0 (in years)")
    if sigma <= 0:
        raise ValueError("volatility must be > 0")


def _d1_d2(
    S: float, K: float, T: float, r: float, q: float, sigma: float
) -> tuple[float, float]:
    """Compute d1 and d2 for Black-Scholes with continuous div yield q."""
    vsqrt = sigma * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / vsqrt
    d2 = d1 - vsqrt
    return d1, d2


def bs_price(opt: OptionSpec, mkt: MarketData) -> float:
    """
    Black-Scholes price for a European call/put with continuous dividend yield.
    Call: C = S e^{-qT} N(d1) - K e^{-rT} N(d2)
    Put : P = K e^{-rT} N(-d2) - S e^{-qT} N(-d1)
    """
    S, K, T = mkt.spot, opt.strike, opt.maturity
    r, q, sigma = mkt.rate, mkt.dividend_yield, mkt.volatility
    _check_inputs(S, K, T, sigma)

    d1, d2 = _d1_d2(S, K, T, r, q, sigma)
    disc_r = math.exp(-r * T)
    disc_q = math.exp(-q * T)

    if opt.option_type == OptionType.CALL:
        return S * disc_q * norm_cdf(d1) - K * disc_r * norm_cdf(d2)
    else:
        return K * disc_r * norm_cdf(-d2) - S * disc_q * norm_cdf(-d1)
