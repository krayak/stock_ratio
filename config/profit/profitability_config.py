# Benchmark ranges - adapted for the Indian market and using ranges
INDUSTRY_ROA_BENCHMARK = {
    "IT Services": (12, 20),  # Higher for IT
    "Software Products": (10, 18),
    "E-commerce": (5, 12), # Varies widely, depends on stage
    "Banks (Private Sector)": (1.0, 1.8), #Lower for banks
    "Banks (Public Sector)": (0.5, 1.2), #Lower for banks
    "NBFCs": (1.2, 2.0),
    "Pharmaceuticals": (10, 18),
    "Healthcare Services": (8, 15),
    "Consumer Durables": (6, 12),
    "Consumer Staples": (8, 14),
    "Automobiles": (4, 10),
    "Cement": (7, 12),
    "Construction": (5, 10),
    "Metals & Mining": (6, 12),
    "Oil & Gas": (4, 8),
    "Power": (4, 9),
    "Telecom": (5, 10),
    "Real Estate": (4, 9),
    "Media & Entertainment": (6, 12),
    "Textiles": (4, 8),
    "Chemicals": (7, 13),
    "FMCG": (10, 16)
}

INDUSTRY_ROE_BENCHMARK = {
    "IT Services": (25, 40),  # Higher for IT
    "Software Products": (20, 35),
    "E-commerce": (10, 20), # Varies widely
    "Banks": (10, 18), #Lower for banks
    "NBFCs": (15, 25),
    "Pharmaceuticals": (18, 30),
    "Healthcare Services": (15, 25),
    "Consumer Durables": (12, 20),
    "Consumer Staples": (14, 22),
    "Automobiles": (8, 16),
    "Cement": (12, 18),
    "Construction": (10, 16),
    "Metals & Mining": (10, 18),
    "Oil & Gas": (8, 15),
    "Power": (7, 12),
    "Telecom": (10, 18),
    "Real Estate": (8, 15),
    "Media & Entertainment": (12, 20),
    "Textiles": (8, 14),
    "Chemicals": (12, 20),
    "FMCG": (16, 25)
}

INDUSTRY_PROFIT_MARGIN_BENCHMARK = { #Net Profit Margin
    "IT Services": (20, 35),
    "Software Products": (15, 30),
    "E-commerce": (0, 10), # Often negative or low in early stages
    "Banks": (20, 35), #Higher for banks
    "NBFCs": (15, 25),
    "Pharmaceuticals": (25, 40),
    "Healthcare Services": (15, 25),
    "Consumer Durables": (8, 15),
    "Consumer Staples": (12, 20),
    "Automobiles": (4, 10),
    "Cement": (10, 18),
    "Construction": (5, 12),
    "Metals & Mining": (8, 15),
    "Oil & Gas": (5, 12),
    "Power": (8, 15),
    "Telecom": (10, 18),
    "Real Estate": (10, 18),
    "Media & Entertainment": (10, 20),
    "Textiles": (5, 12),
    "Chemicals": (10, 18),
    "FMCG": (15, 25)
}

INDUSTRY_GROSS_PROFIT_MARGIN_BENCHMARK = {
    "IT Services": (70, 90),  # Very high for IT services
    "Software Products": (60, 80),
    "E-commerce": (20, 50),  # Highly variable
    "Banks": (50, 70),  # Interest income is major part
    "NBFCs": (60, 80), # Interest income is major part
    "Pharmaceuticals": (60, 80),
    "Healthcare Services": (40, 60),
    "Consumer Durables": (30, 50),
    "Consumer Staples": (30, 50),
    "Automobiles": (15, 30),
    "Cement": (25, 40),
    "Construction": (15, 30),
    "Metals & Mining": (20, 40),
    "Oil & Gas": (20, 40),
    "Power": (20, 40),
    "Telecom": (40, 60),
    "Real Estate": (30, 50),
    "Media & Entertainment": (30, 50),
    "Textiles": (15, 30),
    "Chemicals": (25, 40),
    "FMCG": (30, 50)
}

INDUSTRY_OPERATING_PROFIT_MARGIN_BENCHMARK = {
    "IT Services": (25, 40),
    "Software Products": (20, 35),
    "E-commerce": (-10, 5),  # Often negative in early stages
    "Banks": (25, 40), #Higher for banks
    "NBFCs": (20, 30),
    "Pharmaceuticals": (30, 45),
    "Healthcare Services": (20, 30),
    "Consumer Durables": (10, 18),
    "Consumer Staples": (15, 25),
    "Automobiles": (5, 12),
    "Cement": (12, 20),
    "Construction": (8, 15),
    "Metals & Mining": (10, 18),
    "Oil & Gas": (8, 15),
    "Power": (10, 18),
    "Telecom": (15, 25),
    "Real Estate": (15, 25),
    "Media & Entertainment": (12, 22),
    "Textiles": (8, 15),
    "Chemicals": (12, 20),
    "FMCG": (18, 28)
}

DEFAULT_ROA_BENCHMARK = (5, 10)
DEFAULT_ROE_BENCHMARK = (10, 18)
DEFAULT_PROFIT_MARGIN_BENCHMARK = (10, 18)
DEFAULT_GROSS_PROFIT_MARGIN_BENCHMARK = (30, 50)
DEFAULT_OPERATING_PROFIT_MARGIN_BENCHMARK = (10, 18)
