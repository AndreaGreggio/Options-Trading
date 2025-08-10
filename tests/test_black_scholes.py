import math
from src.options_trading import (
    OptionType,
    OptionSpec,
    MarketData,
    bs_price,
    implied_volatility,
)


def test_atm_call_price_known_value():
    opt = OptionSpec(OptionType.CALL, 100.0, 1.0)
    mkt = MarketData(spot=100.0, rate=0.05, dividend_yield=0.0, volatility=0.20)
    price = bs_price(opt, mkt)
    assert abs(price - 10.4506) < 1e-3


def test_put_call_parity():
    call = OptionSpec(OptionType.CALL, 100.0, 1.0)
    put = OptionSpec(OptionType.PUT, 100.0, 1.0)
    mkt = MarketData(spot=100.0, rate=0.05, dividend_yield=0.0, volatility=0.20)
    c = bs_price(call, mkt)
    p = bs_price(put, mkt)
    lhs = c - p
    rhs = mkt.spot * math.exp(-mkt.dividend_yield * 1.0) - 100.0 * math.exp(
        -mkt.rate * 1.0
    )
    assert abs(lhs - rhs) < 1e-6


def test_implied_vol_recovery():
    opt = OptionSpec(OptionType.PUT, 120.0, 0.5)
    mkt = MarketData(spot=100.0, rate=0.01, dividend_yield=0.0, volatility=0.35)
    price = bs_price(opt, mkt)
    iv = implied_volatility(opt, mkt, price)
    assert abs(iv - 0.35) < 1e-4
