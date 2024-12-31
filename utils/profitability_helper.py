from config.profit.profitability_config import (
    INDUSTRY_ROA_BENCHMARK,
    INDUSTRY_ROE_BENCHMARK,
    INDUSTRY_PROFIT_MARGIN_BENCHMARK,
    INDUSTRY_GROSS_PROFIT_MARGIN_BENCHMARK,
    INDUSTRY_OPERATING_PROFIT_MARGIN_BENCHMARK
)

def get_industry_roa_benchmark(industry: str):
    return INDUSTRY_ROA_BENCHMARK.get(industry, 10)  # Default to 10% if sector not found

def get_industry_roe_benchmark(industry: str):
    return INDUSTRY_ROE_BENCHMARK.get(industry, 15)  # Default to 15% if sector not found

def get_industry_net_profit_margin_benchmark(industry: str):
    return INDUSTRY_PROFIT_MARGIN_BENCHMARK.get(industry, 10)  # Default to 10%

def get_industry_gross_profit_margin_benchmark(industry: str):
    return INDUSTRY_GROSS_PROFIT_MARGIN_BENCHMARK.get(industry, 40)