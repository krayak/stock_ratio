import yfinance as yf
import math
from config.liquidity.liquidity_config import (
    INDUSTRY_CURRENT_RATIO_BENCHMARK,
    INDUSTRY_QUICK_RATIO_BENCHMARK,
    DEFAULT_CURRENT_RATIO_BENCHMARK,
    DEFAULT_QUICK_RATIO_BENCHMARK
)
from utils.benchmark import (
    get_industry_benchmark
)


class LiquidityRatios:
    def __init__(self, ticker):
        """
        Initialize with the stock ticker and fetch relevant financial data.
        """
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self.info = self.stock.info
        self.balance_sheet = self.stock.balance_sheet
        # print(f"Balance Sheet for {ticker}:\n{self.balance_sheet}")

    def _get_recommendation_by_range(self, value, benchmark_range, buy_if_below=True):
        if value is None or benchmark_range is None:
            return "Data Unavailable"
        try:
            lower_bound, upper_bound = benchmark_range
        except TypeError: #Handle the case where benchmark_range is not a tuple
            return "Data Unavailable"

        if buy_if_below:
            if value < lower_bound:
                return "Buy"
            elif value > upper_bound:
                return "Sell"
            else:
                return "Hold"
        else:
            if value > upper_bound:
                return "Buy"
            elif value < lower_bound:
                return "Sell"
            else:
                return "Hold"
            
    def _compare_to_benchmark(self, value, benchmark_range):
        if value is None or benchmark_range is None:
            return "Data Unavailable"
        try:
            lower_bound, upper_bound = benchmark_range
        except TypeError:
            return "Data Unavailable"

        if value > upper_bound:
            return "Above Benchmark"
        elif value < lower_bound:
            return "Below Benchmark"
        else:
            return "Within Benchmark"

    def _get_benchmark(self, ratio_type):
        sector = self.info.get("sector")
        industry = self.info.get("industry")
        if ratio_type == "Current Ratio":
            return get_industry_benchmark(sector, industry, INDUSTRY_CURRENT_RATIO_BENCHMARK, DEFAULT_CURRENT_RATIO_BENCHMARK)
        elif ratio_type == "Quick Ratio":
            return get_industry_benchmark(sector, industry, INDUSTRY_QUICK_RATIO_BENCHMARK, DEFAULT_QUICK_RATIO_BENCHMARK)
        else:
            return None
        
    def _get_financial_data(self, keys):
        """
        Generic function to get financial data given a list of possible keys.
        """
        if self.balance_sheet is None or self.balance_sheet.empty:
            return None
        for key in keys:
            try:
                value = self.balance_sheet.loc[key].iloc[0]
                if not (isinstance(value, (int, float)) and not math.isnan(value)):
                    continue # Skip if value is not a valid number
                return value
            except KeyError:
                continue
        return None

    def _calculate_ratio(self, numerator, denominator):
        """
        Utility function to calculate a ratio and handle zero or None values.
        """
        if numerator is None or denominator is None or denominator == 0:
            return None
        return numerator / denominator

    def get_current_assets(self):
        possible_keys = [
            "Total Current Assets", "Current Assets", "totalCurrentAssets", "currentAssets",
            "Total Assets", "totalAssets", "Assets" # Fallback if only total assets are available
        ]
        return self._get_financial_data(possible_keys)

    def get_current_liabilities(self):
        possible_keys = [
            "Total Current Liabilities", "Current Liabilities", "totalCurrentLiabilities", "currentLiabilities"
        ]
        return self._get_financial_data(possible_keys)

    def get_inventory(self):
        possible_keys = ["Inventory", "inventory", "Inventories"]
        return self._get_financial_data(possible_keys)

    def calculate_current_ratio(self):
        """Calculate and evaluate Current Ratio."""
        try:
            current_assets = self.get_current_assets()
            if current_assets is None:
                return {"Current Ratio": None, "Industry Benchmark": None, "Comparison": "Current Assets Data Unavailable", "Recommendation": "Current Assets Data Unavailable"} 
            current_liabilities = self.get_current_liabilities()
            if current_liabilities is None:
                return {"Current Ratio": None, "Industry Benchmark": None, "Comparison": "Current Liabilities Data Unavailable", "Recommendation": "Current Liabilities Data Unavailable"}

            # Calculate Current Ratio
            current_ratio = self._calculate_ratio(current_assets, current_liabilities)
            benchmark_range = self._get_benchmark("Current Ratio")
            comparison = self._compare_to_benchmark(current_ratio, benchmark_range)
            recommendation = self._get_recommendation_by_range(current_ratio, benchmark_range)
            return {
                "Current Ratio": round(current_ratio, 2) if current_ratio is not None else None,
                "Industry Benchmark": benchmark_range,
                "Comparison": comparison,
                "Recommendation": recommendation
            }
        except Exception as e:
            return {"error": f"Error calculating Current Ratio: {str(e)}"}

    def calculate_quick_ratio(self):
        """Calculate and evaluate Quick Ratio."""
        try:
            current_assets = self.get_current_assets()
            inventory = self.get_inventory()
            current_liabilities = self.get_current_liabilities()

            if current_assets is None:
                return {"Quick Ratio": None, "Industry Benchmark": None, "Comparison": "Current Assets Data Unavailable", "Recommendation": "Current Assets Data Unavailable"}
            if inventory is None:
                return {"Quick Ratio": None, "Industry Benchmark": None, "Comparison": "Inventory Data Unavailable", "Recommendation": "Inventory Data Unavailable"}
            if current_liabilities is None:
                return {"Quick Ratio": None, "Industry Benchmark": None, "Comparison": "Current Liabilities Data Unavailable", "Recommendation": "Current Liabilities Data Unavailable"}

            # Calculate Quick Assets (Current Assets - Inventory)
            quick_assets = None if current_assets is None or inventory is None else current_assets - inventory
            quick_ratio = self._calculate_ratio(quick_assets, current_liabilities)
            benchmark_range = self._get_benchmark("Quick Ratio")
            comparison = self._compare_to_benchmark(quick_ratio, benchmark_range)
            recommendation = self._get_recommendation_by_range(quick_ratio, benchmark_range)
            return {
                "Quick Ratio": round(quick_ratio, 2) if quick_ratio is not None else None,
                "Industry Benchmark": benchmark_range,
                "Comparison": comparison,
                "Recommendation": recommendation
            }
        except Exception as e:
            return {"Quick Ratio": None, "Industry Benchmark": None, "Comparison": f"Error calculating Quick Ratio: {str(e)}", "Recommendation": f"Error calculating Quick Ratio: {str(e)}"}

    def fetch_all_ratios(self):
        """Fetch and return all liquidity ratios with benchmarks and recommendations."""
        ratios = {
            "Current Ratio": self.calculate_current_ratio,
            "Quick Ratio": self.calculate_quick_ratio,
        }
        results = {}
        for ratio_name, calculation_method in ratios.items():
            results[ratio_name] = calculation_method()  # Call each calculation method
        return results
