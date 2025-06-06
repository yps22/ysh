from dataclasses import dataclass
from typing import Optional

@dataclass
class DamageParams:
    monthly_income: float
    months: int
    disability_rate: float
    prior_disability_rate: float = 0.0
    past_medical: float = 0.0
    future_medical: float = 0.0
    pain_compensation: float = 0.0
    liability_ratio: float = 1.0
    discount_rate: float = 0.05  # annual interest rate used for discounting


def hoffman_simple_present_value(monthly_amount: float, months: int, annual_rate: float = 0.05) -> float:
    """Calculate present value of a series of monthly payments using Hoffmann's
    simple interest discount method.

    Parameters
    ----------
    monthly_amount: float
        Amount received each month.
    months: int
        Number of months to consider. Any fractional part should be rounded
        according to the desired policy before calling this function.
    annual_rate: float, optional
        Annual discount rate (e.g., 0.05 for 5%). Default is 5%.

    Returns
    -------
    float
        Present value of all future payments.
    """
    rate_per_month = annual_rate / 12
    pv = 0.0
    for m in range(1, months + 1):
        pv += monthly_amount / (1 + rate_per_month * m)
    return pv


def calculate_damages(params: DamageParams) -> float:
    """Compute total damages based on provided parameters."""
    net_disability = max(params.disability_rate - params.prior_disability_rate, 0)
    lost_income = hoffman_simple_present_value(
        params.monthly_income * net_disability,
        params.months,
        params.discount_rate,
    )
    total = lost_income + params.past_medical + params.future_medical + params.pain_compensation
    return total * params.liability_ratio


if __name__ == "__main__":
    # Example usage with hypothetical numbers
    params = DamageParams(
        monthly_income=2000000,  # average monthly income
        months=240,              # number of months until retirement
        disability_rate=0.85,    # total disability after accident
        prior_disability_rate=0.24,  # pre-existing disability
        past_medical=408939,
        future_medical=0,
        pain_compensation=10000000,
        liability_ratio=0.8,
    )
    print(f"Estimated damages: {calculate_damages(params):,.0f} KRW")
