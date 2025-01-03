INDUSTRY_ASSET_TURNOVER_RATIO_BENCHMARK = {
    "IT Services": (0.8, 1.5),  # Lower asset intensity
    "Software Products": (0.7, 1.4),
    "E-commerce": (1.0, 2.5),  # Higher turnover due to sales volume
    "Banks (Private Sector)": (0.01, 0.02),  # Very low, assets are primarily loans
    "Banks (Public Sector)": (0.005, 0.015),
    "NBFCs": (0.05, 0.15),
    "Pharmaceuticals": (0.5, 1.0),
    "Healthcare Services": (0.6, 1.2),
    "Consumer Durables": (1.0, 2.0),
    "Consumer Staples": (0.8, 1.5),
    "Automobiles": (1.0, 1.8),
    "Cement": (0.5, 1.0),
    "Construction": (0.8, 1.5),
    "Metals & Mining": (0.6, 1.2),
    "Oil & Gas": (0.4, 0.8),
    "Power": (0.3, 0.7),
    "Telecom": (0.4, 0.9),
    "Real Estate": (0.2, 0.5), # Very low, assets are long term
    "Media & Entertainment": (0.7, 1.4),
    "Textiles": (1.0, 1.8),
    "Chemicals": (0.7, 1.3),
    "FMCG": (1.0, 1.8)
}

INDUSTRY_INVENTORY_TURNOVER_RATIO_BENCHMARK = {
    "IT Services": (None, None),  # Not applicable (minimal inventory)
    "Software Products": (None, None), # Not applicable
    "E-commerce": (5, 15),  # High turnover expected
    "Banks (Private Sector)": (None, None),  # Not applicable
    "Banks (Public Sector)": (None, None),
    "NBFCs": (None, None),
    "Pharmaceuticals": (3, 8),
    "Healthcare Services": (None, None), # Low or not applicable
    "Consumer Durables": (3, 6),
    "Consumer Staples": (5, 10),
    "Automobiles": (4, 8),
    "Cement": (4, 8),
    "Construction": (None, None), # Low or not applicable
    "Metals & Mining": (3, 6),
    "Oil & Gas": (4, 8),
    "Power": (None, None),
    "Telecom": (None, None),
    "Real Estate": (None, None),
    "Media & Entertainment": (None, None),
    "Textiles": (4, 8),
    "Chemicals": (4, 9),
    "FMCG": (6, 12)
}

INDUSTRY_RECEIVABLES_TURNOVER_RATIO_BENCHMARK = {
    "IT Services": (6, 12),  # Efficient collection expected
    "Software Products": (5, 10),
    "E-commerce": (10, 20),  # Often high due to credit sales
    "Banks (Private Sector)": (None, None),  # Not directly applicable (different metrics used)
    "Banks (Public Sector)": (None, None),
    "NBFCs": (None, None),
    "Pharmaceuticals": (4, 8),
    "Healthcare Services": (5, 10),
    "Consumer Durables": (4, 8),
    "Consumer Staples": (8, 15), # Higher due to credit terms offered
    "Automobiles": (6, 12),
    "Cement": (5, 10),
    "Construction": (3, 6), # Can be lower due to project timelines
    "Metals & Mining": (4, 8),
    "Oil & Gas": (6, 12),
    "Power": (6, 12),
    "Telecom": (4, 8),
    "Real Estate": (3, 6),
    "Media & Entertainment": (5, 10),
    "Textiles": (4, 8),
    "Chemicals": (5, 10),
    "FMCG": (10, 18)
}

DEFAULT_ASSET_TURNOVER_RATIO_BENCHMARK = (0.5, 1.0)
DEFAULT_INVENTORY_TURNOVER_RATIO_BENCHMARK = (3, 6)
DEFAULT_RECEIVABLES_TURNOVER_RATIO_BENCHMARK = (4, 8)