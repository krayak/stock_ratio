from config.liquidity.liquidity_config import (
    INDUSTRY_CURRENT_RATIO_BENCHMARK,
    INDUSTRY_QUICK_RATIO_BENCHMARK,
)

def get_industry_current_ratio_benchmark(industry: str):
    return INDUSTRY_CURRENT_RATIO_BENCHMARK.get(industry, 2)  # Default to 10% if sector not found

def get_industry_quick_ratio_benchmark(industry: str):
    return INDUSTRY_QUICK_RATIO_BENCHMARK.get(industry, 1)  # Default to 15% if sector not found
