from config.valuation.valuation_config import (
    INDUSTRY_PE_BENCHMARKS, 
    DEFAULT_PE_BENCHMARK, 
    INDUSTRY_PB_BENCHMARK,
    INDUSTRY_PS_BENCHMARK,
    INDUSTRY_PEG_BENCHMARK,
    INDUSTRY_DIVIDEND_YIELD_BENCHMARK,
    INDUSTRY_DIVIDEND_PAYOUT_RATIO_BENCHMARK
    )

def get_industry_pe_benchmark(industry, sector):
    """
    Retrieve the P/E benchmark for the given industry or sector.

    Args:
        industry (str): The industry of the company.
        sector (str): The sector of the company.

    Returns:
        float: The P/E benchmark for the given industry or sector.
    """
    # Check if the industry is in the benchmark dictionary
    if industry in INDUSTRY_PE_BENCHMARKS:
        return INDUSTRY_PE_BENCHMARKS[industry]
    # Check if the sector is in the benchmark dictionary
    elif sector in INDUSTRY_PE_BENCHMARKS:
        return INDUSTRY_PE_BENCHMARKS[sector]
    else:
        # Return the default P/E benchmark if neither industry nor sector are found
        return DEFAULT_PE_BENCHMARK

def get_industry_pb_benchmark(industry: str):
    """
    Helper function to get the industry P/B benchmark.
    If the industry is not found in the config, return None.
    """
    return INDUSTRY_PB_BENCHMARK.get(industry, None)

def get_industry_ps_benchmark(industry: str):
    """
    Helper function to get the industry P/S benchmark.
    If the industry is not found in the config, return None.
    """
    return INDUSTRY_PS_BENCHMARK.get(industry, None)

def get_industry_peg_benchmark(industry: str):
    """
    Helper function to get the industry PEG benchmark.
    If the industry is not found in the config, return None.
    """
    return INDUSTRY_PEG_BENCHMARK.get(industry, None)

def get_industry_dividend_yield_benchmark(industry: str):
    """
    Helper function to get the industry Dividend Yield benchmark.
    If the industry is not found in the config, return None.
    """
    return INDUSTRY_DIVIDEND_YIELD_BENCHMARK.get(industry, None)

def get_industry_dividend_payout_ratio_benchmark(industry):
    # Return the benchmark value for the given industry, or a default value if not found
    return INDUSTRY_DIVIDEND_PAYOUT_RATIO_BENCHMARK.get(industry, 0.0)