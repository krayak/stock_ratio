INDUSTRY_DEBT_TO_EQUITY_RATIO_BENCHMARK = {
    "IT Services": (0.2, 0.8),  # Can be slightly higher in India due to growth
    "Software Products": (0.1, 0.6),
    "E-commerce": (0.7, 2.0),  # Higher due to funding rounds, more volatile
    "Banks (Private Sector)": (6, 12),  # Reflects Indian banking norms
    "Banks (Public Sector)": (9, 18),
    "NBFCs": (4, 9),  # Higher due to their business model
    "Pharmaceuticals": (0.6, 1.5),
    "Healthcare Services": (0.5, 1.2),
    "Consumer Durables": (0.7, 1.6),
    "Consumer Staples": (0.5, 1.2),
    "Automobiles": (0.9, 1.8),
    "Cement": (1.2, 2.5),
    "Construction": (1.5, 3.5),  # Higher due to project financing
    "Metals & Mining": (1.0, 2.0),
    "Oil & Gas": (0.8, 1.8),
    "Power": (2.0, 4.0),  # Higher due to large infrastructure projects
    "Telecom": (1.2, 2.5),
    "Real Estate": (2.0, 4.0),
    "Media & Entertainment": (0.7, 1.6),
    "Textiles": (1.2, 2.5),
    "Chemicals": (0.8, 1.8),
    "FMCG": (0.4, 1.0)
}

INDUSTRY_INTEREST_COVERAGE_RATIO_BENCHMARK = {
    "IT Services": (8, 18),  # Still high, but can be slightly lower
    "Software Products": (6, 12),
    "E-commerce": (2, 6),  # Can be lower due to reinvestment of profits
    "Banks (Private Sector)": (None, None),  # Not directly applicable
    "Banks (Public Sector)": (None, None),
    "NBFCs": (None, None),
    "Pharmaceuticals": (4, 10),
    "Healthcare Services": (3, 8),
    "Consumer Durables": (3, 7),
    "Consumer Staples": (5, 10),
    "Automobiles": (3, 7),
    "Cement": (2, 5),
    "Construction": (1.5, 4),
    "Metals & Mining": (2, 6),
    "Oil & Gas": (3, 8),
    "Power": (1.5, 4),
    "Telecom": (2, 6),
    "Real Estate": (1.5, 4),
    "Media & Entertainment": (3, 8),
    "Textiles": (2, 6),
    "Chemicals": (3, 9),
    "FMCG": (6, 12)
}

DEFAULT_DEBT_TO_EQUITY_RATIO_BENCHMARK = (0.6, 1.2)  # Adjusted default
DEFAULT_INTEREST_COVERAGE_RATIO_BENCHMARK = (3, 6)  # Adjusted default