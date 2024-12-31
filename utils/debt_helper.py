from config.debt.debt_config import (
    INDUSTRY_DEBT_TO_EQUITY_RATIO_BENCHMARK,
    INDUSTRY_INTEREST_COVERAGE_RATIO_BENCHMARK,
)

def get_industry_debt_to_equity_benchmark(industry: str):
    return INDUSTRY_DEBT_TO_EQUITY_RATIO_BENCHMARK.get(industry, 10)  # Default to 10% if sector not found

def get_industry_interest_coverage_benchmark(industry: str):
    return INDUSTRY_INTEREST_COVERAGE_RATIO_BENCHMARK.get(industry, 15) 