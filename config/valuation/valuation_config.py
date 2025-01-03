# valuation_config.py

# Benchmark ranges are now based on more researched (but still generalized) values
# These are still not definitive and require your own research for specific stocks

INDUSTRY_PE_BENCHMARKS = {
    "IT Services": (20, 30),  # Slightly adjusted
    "Software Products": (25, 40),
    "E-commerce": (35, 50),  # More realistic for high growth
    "Banks (Private Sector)": (10, 16),
    "Banks (Public Sector)": (7, 11),
    "NBFCs": (12, 20),
    "Pharmaceuticals": (18, 28),
    "Healthcare Services": (22, 32),
    "Consumer Durables": (18, 28),
    "Consumer Staples": (14, 22),
    "Automobiles": (14, 22),
    "Cement": (16, 22),
    "Construction": (13, 20),
    "Metals & Mining": (8, 12),  # Reflects cyclicality
    "Oil & Gas": (7, 10),      # Reflects cyclicality
    "Power": (9, 14),
    "Telecom": (10, 16),
    "Real Estate": (13, 20),
    "Media & Entertainment": (18, 28),
    "Textiles": (8, 15),
    "Chemicals": (13, 22),
    "FMCG": (18, 28)
}

DEFAULT_PE_BENCHMARK = (18, 25)  # Adjusted default

INDUSTRY_PB_BENCHMARK = {
    "Banks": (0.8, 1.5),  # More conservative
    "NBFCs": (1.2, 2.5),
    "IT Services": (2.5, 5.0),
    "Pharmaceuticals": (1.8, 3.5),
    "Manufacturing": (1.2, 2.5),
    "Consumer": (1.8, 3.5),
    "Real Estate": (0.8, 2.0),
    "Infrastructure": (1.0, 2.0),
    "Metals": (0.6, 1.2),
    "Energy": (0.8, 1.5)
}

INDUSTRY_PS_BENCHMARK = {
    "IT Services": (2.5, 5.0),
    "E-commerce": (4.0, 8.0),
    "Pharmaceuticals": (2.5, 4.0),
    "Consumer": (1.5, 3.0),
    "Manufacturing": (0.8, 2.0),
    "Metals": (0.6, 1.2),
    "Energy": (0.8, 1.5),
    "FMCG": (2.5, 4.0)
}

INDUSTRY_PEG_BENCHMARK = {
    "IT Services": (0.8, 1.2), #More conservative
    "Pharmaceuticals": (0.8, 1.1),
    "Consumer": (0.7, 1.0),
    "Manufacturing": (0.6, 0.9)
}

INDUSTRY_DIVIDEND_YIELD_BENCHMARK = {
    "Utilities": (3.5, 5.5),  # Slightly higher
    "Telecom": (3.0, 4.5),
    "FMCG": (0.8, 2.0), # Adjusted
    "Banks": (1.0, 2.5),
    "NBFCs": (0.5, 1.5),
    "Energy": (2.5, 4.5)
}

INDUSTRY_DIVIDEND_PAYOUT_RATIO_BENCHMARK = {
    "Utilities": (55, 75),  # Slightly higher
    "FMCG": (35, 55),
    "Banks": (35, 55),
    "NBFCs": (25, 45),
    "Energy": (45, 65)
}

