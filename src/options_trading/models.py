from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class OptionType(str, Enum):
    CALL = "CALL"
    PUT = "PUT"


@dataclass(frozen=True)
class OptionSpec:
    """Contract terms for a European option."""

    option_type: OptionType
    # ticker: str  # e.g. "AAPL"
    strike: float  # K
    maturity: float  # T, in years


@dataclass(frozen=True)
class MarketData:
    """Market inputs for Black-Scholes with continuous dividend yield."""

    spot: float  # S
    rate: float  # r, continuously compounded (e.g. 0.05 for 5%)
    dividend_yield: float = 0.0  # q, continuously compounded
    volatility: float = 0.2  # sigma as a decimal (e.g. 0.2 for 20%)
    stocksplit: bool = False
