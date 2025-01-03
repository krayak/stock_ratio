SECTOR_TO_INDUSTRY_MAPPING = {
    "Technology": ["IT Services", "Software Products", "E-commerce"],
    "Financial Services": ["Banks (Private Sector)", "Banks (Public Sector)", "NBFCs"],
    "Healthcare": ["Pharmaceuticals", "Healthcare Services"],
    "Consumer Cyclical": ["Consumer Durables", "Automobiles", "Media & Entertainment"],
    "Consumer Defensive": ["Consumer Staples", "FMCG"],
    "Basic Materials": ["Cement", "Metals & Mining", "Chemicals"],
    "Energy": ["Oil & Gas"],
    "Utilities": ["Power"],
    "Communication Services": ["Telecom"],
    "Real Estate": ["Real Estate"],
    "Industrials": ["Construction", "Textiles"]
}

def get_industry_benchmark(sector, industry, benchmark_dict, default_benchmark):
    """Retrieves industry benchmark with robust sector averaging (if needed)."""
    try:
        if industry and industry in benchmark_dict:
            return benchmark_dict[industry]

        elif sector and sector in SECTOR_TO_INDUSTRY_MAPPING:
            industries = SECTOR_TO_INDUSTRY_MAPPING[sector]
            valid_benchmarks = []  # Store valid benchmarks only

            for ind in industries:
                benchmark = benchmark_dict.get(ind) #Use .get to prevent key errors
                if benchmark is not None and isinstance(benchmark, tuple) and all(isinstance(x, (int, float)) for x in benchmark) and len(benchmark) == 2:
                    valid_benchmarks.append(benchmark) # Only add valid benchmarks

            if valid_benchmarks:
                total_lower = sum(lower for lower, upper in valid_benchmarks)
                total_upper = sum(upper for lower, upper in valid_benchmarks)
                return (total_lower / len(valid_benchmarks), total_upper / len(valid_benchmarks))
            else:
                print(f"No valid benchmarks found for sector: {sector}. Using default benchmark")
                return default_benchmark
        else:
            return default_benchmark

    except Exception as e:
        print(f"Error getting benchmark: {e}")
        return default_benchmark
