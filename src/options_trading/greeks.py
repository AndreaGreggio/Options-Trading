from __future__ import annotations
import math
from .models import OptionSpec, MarketData, OptionType
from .stats import norm_pdf, norm_cdf
from .black_scholes import _d1_d2, _check_inputs


def _common(S, K, T, r, q, sigma):
    _check_inputs(S, K, T, sigma)
    d1, d2 = _d1_d2(S, K, T, r, q, sigma)
    disc_r = math.exp(-r * T)
    disc_q = math.exp(-q * T)
    return d1, d2, disc_r, disc_q


def bs_delta(opt: OptionSpec, mkt: MarketData) -> float:
    S, K, T = mkt.spot, opt.strike, opt.maturity
    r, q, sigma = mkt.rate, mkt.dividend_yield, mkt.volatility
    d1, _, _, disc_q = _common(S, K, T, r, q, sigma)
    if opt.option_type is OptionType.CALL:
        return disc_q * norm_cdf(d1)
    else:
        return disc_q * (norm_cdf(d1) - 1.0)


def bs_gamma(opt: OptionSpec, mkt: MarketData) -> float:
    S, K, T = mkt.spot, opt.strike, opt.maturity
    r, q, sigma = mkt.rate, mkt.dividend_yield, mkt.volatility
    d1, _, _, disc_q = _common(S, K, T, r, q, sigma)
    return disc_q * norm_pdf(d1) / (S * sigma * math.sqrt(T))


def bs_vega(opt: OptionSpec, mkt: MarketData) -> float:
    S, K, T = mkt.spot, opt.strike, opt.maturity
    r, q, sigma = mkt.rate, mkt.dividend_yield, mkt.volatility
    d1, _, _, disc_q = _common(S, K, T, r, q, sigma)
    return S * disc_q * norm_pdf(d1) * math.sqrt(T)


def bs_theta(opt: OptionSpec, mkt: MarketData) -> float:
    """
    Theta per YEAR (divide by 365 for per-day).
    """
    S, K, T = mkt.spot, opt.strike, opt.maturity
    r, q, sigma = mkt.rate, mkt.dividend_yield, mkt.volatility
    d1, d2, disc_r, disc_q = _common(S, K, T, r, q, sigma)

    first = -S * disc_q * norm_pdf(d1) * sigma / (2.0 * math.sqrt(T))
    if opt.option_type is OptionType.CALL:
        return first - r * K * disc_r * norm_cdf(d2) + q * S * disc_q * norm_cdf(d1)
    else:
        return first + r * K * disc_r * norm_cdf(-d2) - q * S * disc_q * norm_cdf(-d1)


def bs_rho(opt: OptionSpec, mkt: MarketData) -> float:
    S, K, T = mkt.spot, opt.strike, opt.maturity
    r, q, sigma = mkt.rate, mkt.dividend_yield, mkt.volatility
    _, d2, disc_r, _ = _common(S, K, T, r, q, sigma)
    if opt.option_type is OptionType.CALL:
        return K * T * disc_r * norm_cdf(d2)
    else:
        return -K * T * disc_r * norm_cdf(-d2)
