from src.options_trading import (
    OptionType,
    OptionSpec,
    MarketData,
    bs_price,
    bs_delta,
    bs_gamma,
    bs_vega,
    bs_theta,
    bs_rho,
    implied_volatility,
)

# Example: S=100, K=100, T=1y, r=5%, q=0%, sigma=20%
opt = OptionSpec(option_type=OptionType.CALL, strike=100.0, maturity=1.0)
mkt = MarketData(spot=100.0, rate=0.05, dividend_yield=0.0, volatility=0.20)

price = bs_price(opt, mkt)
print(f"Call price: {price:.4f}")

print("Greeks:")
print("  Delta:", bs_delta(opt, mkt))
print("  Gamma:", bs_gamma(opt, mkt))
print("  Vega :", bs_vega(opt, mkt))
print("  Theta:", bs_theta(opt, mkt))  # per year
print("  Rho  :", bs_rho(opt, mkt))

# Back out IV from the observed price:
iv = implied_volatility(opt, mkt, target_price=price)
print(f"Implied volatility (should be ~0.20): {iv:.4f}")
