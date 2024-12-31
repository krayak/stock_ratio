from config.efficiency.efficiency_config import (
    INDUSTRY_ASSET_TURNOVER_RATIO_BENCHMARK,
    INDUSTRY_INVENTORY_TURNOVER_RATIO_BENCHMARK
)

def get_industry_asset_turnover_benchmark(industry: str):
    """
    Fetch the industry benchmark for Asset Turnover Ratio.
    Defaults to 1 if the industry is not found in the configuration.
    """
    return INDUSTRY_ASSET_TURNOVER_RATIO_BENCHMARK.get(industry, 1)  # Default to 1 if sector not found

def get_industry_inventory_turnover_benchmark(industry: str):
    """
    Fetch the industry benchmark for Inventory Turnover Ratio.
    Defaults to 10 if the industry is not found in the configuration.
    """
    return INDUSTRY_INVENTORY_TURNOVER_RATIO_BENCHMARK.get(industry, 10)  # Default to 10 if sector not found
