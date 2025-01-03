INDUSTRY_CURRENT_RATIO_BENCHMARK = {
    "IT Services": (2.0, 3.0),  # Typically higher
    "Software Products": (1.8, 2.8),
    "E-commerce": (1.2, 2.0),  # Can vary widely
    "Banks (Private Sector)": (0.8, 1.2),  # Lower for banks
    "Banks (Public Sector)": (0.7, 1.1),  # Lower for banks
    "NBFCs": (1.0, 1.5),
    "Pharmaceuticals": (1.5, 2.5),
    "Healthcare Services": (1.2, 2.0),
    "Consumer Durables": (1.0, 1.8),
    "Consumer Staples": (1.2, 2.0),
    "Automobiles": (1.0, 1.6),
    "Cement": (1.0, 1.5),
    "Construction": (0.8, 1.4),
    "Metals & Mining": (1.0, 1.6),
    "Oil & Gas": (0.8, 1.4),
    "Power": (0.8, 1.2),
    "Telecom": (0.9, 1.5),
    "Real Estate": (0.7, 1.2),
    "Media & Entertainment": (1.0, 1.8),
    "Textiles": (0.8, 1.4),
    "Chemicals": (1.1, 1.8),
    "FMCG": (1.2, 2.0)
}

INDUSTRY_QUICK_RATIO_BENCHMARK = {
    "IT Services": (1.5, 2.5),  # Lower than current ratio due to less inventory
    "Software Products": (1.2, 2.2),
    "E-commerce": (0.8, 1.5),  # Can be very low due to fast inventory turnover
    "Banks (Private Sector)": (0.5, 0.8),  # Even lower, focus is on liquid assets
    "Banks (Public Sector)": (0.4, 0.7),  # Even lower, focus is on liquid assets
    "NBFCs": (0.7, 1.2),
    "Pharmaceuticals": (1.0, 2.0),
    "Healthcare Services": (0.9, 1.6),
    "Consumer Durables": (0.7, 1.4),
    "Consumer Staples": (0.8, 1.6),
    "Automobiles": (0.7, 1.2),
    "Cement": (0.7, 1.2),
    "Construction": (0.5, 1.0),
    "Metals & Mining": (0.7, 1.2),
    "Oil & Gas": (0.6, 1.0),
    "Power": (0.6, 1.0),
    "Telecom": (0.7, 1.2),
    "Real Estate": (0.4, 0.8),
    "Media & Entertainment": (0.7, 1.4),
    "Textiles": (0.5, 1.0),
    "Chemicals": (0.8, 1.4),
    "FMCG": (0.8, 1.6)
}

DEFAULT_CURRENT_RATIO_BENCHMARK = (1.0, 2.0)
DEFAULT_QUICK_RATIO_BENCHMARK = (0.7, 1.5)