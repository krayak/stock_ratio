import yfinance as yf
from utils.liquidity_helper import (
    get_industry_current_ratio_benchmark,
    get_industry_quick_ratio_benchmark
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

    def _get_benchmark(self, ratio_name):
        """
        Fetch the industry benchmark for a given ratio.
        """
        benchmark_functions = {
            "Current Ratio": get_industry_current_ratio_benchmark,
            "Quick Ratio": get_industry_quick_ratio_benchmark,
        }
        sector = self.info.get("sector")
        benchmark_function = benchmark_functions.get(ratio_name)
    
        if benchmark_function and sector:
            return benchmark_function(sector)
        return None

    def _get_latest_financial_value(self, statement, key):
        """
        Utility function to fetch the latest financial value for a given key.
        """
        try:
            return statement.loc[key][0]
        except KeyError:
            return None

    def _calculate_ratio(self, numerator, denominator):
        """
        Utility function to calculate a ratio and handle zero or None values.
        """
        if numerator is None or denominator is None or denominator == 0:
            return None
        return numerator / denominator

    def _get_recommendation(self, ratio, benchmark):
        """
        Generate a recommendation based on the comparison of the ratio to the industry benchmark.
        """
        if ratio is None or benchmark is None:
            return "Data Unavailable"
        elif ratio > benchmark:
            return "Above Benchmark - Positive"
        elif ratio < benchmark:
            return "Below Benchmark - Negative"
        else:
            return "At Benchmark - Neutral"

    def get_current_assets(self):
        """Fetch the latest Current Assets."""
        return self._get_latest_financial_value(self.balance_sheet, 'Total Current Assets')

    def get_current_liabilities(self):
        """Fetch the latest Current Liabilities."""
        return self._get_latest_financial_value(self.balance_sheet, 'Total Current Liabilities')

    def get_inventory(self):
        """Fetch the latest Inventory value."""
        return self._get_latest_financial_value(self.balance_sheet, 'Inventory')

    def calculate_current_ratio(self):
        """Calculate and evaluate Current Ratio."""
        try:
            current_assets = self.get_current_assets()
            current_liabilities = self.get_current_liabilities()

            # Calculate Current Ratio
            current_ratio = self._calculate_ratio(current_assets, current_liabilities)
            current_ratio_benchmark = self._get_benchmark("Current Ratio")
            recommendation = self._get_recommendation(current_ratio, current_ratio_benchmark)

            return {
                "Current Ratio": round(current_ratio, 2) if current_ratio is not None else "N/A",
                "Industry Benchmark": round(current_ratio_benchmark, 2) if current_ratio_benchmark else "N/A",
                "Comparison": (
                    "Above Benchmark" if current_ratio is not None and current_ratio > current_ratio_benchmark else
                    "Below Benchmark" if current_ratio is not None and current_ratio < current_ratio_benchmark else
                    "At Benchmark" if current_ratio is not None and current_ratio == current_ratio_benchmark else
                    "Benchmark Unavailable"
                ),
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

            # Calculate Quick Assets (Current Assets - Inventory)
            quick_assets = None if current_assets is None or inventory is None else current_assets - inventory
            quick_ratio = self._calculate_ratio(quick_assets, current_liabilities)
            quick_ratio_benchmark = self._get_benchmark("Quick Ratio")
            recommendation = self._get_recommendation(quick_ratio, quick_ratio_benchmark)

            return {
                "Quick Ratio": round(quick_ratio, 2) if quick_ratio is not None else "N/A",
                "Industry Benchmark": round(quick_ratio_benchmark, 2) if quick_ratio_benchmark else "N/A",
                "Comparison": (
                    "Above Benchmark" if quick_ratio is not None and quick_ratio > quick_ratio_benchmark else
                    "Below Benchmark" if quick_ratio is not None and quick_ratio < quick_ratio_benchmark else
                    "At Benchmark" if quick_ratio is not None and quick_ratio == quick_ratio_benchmark else
                    "Benchmark Unavailable"
                ),
                "Recommendation": recommendation
            }
        except Exception as e:
            return {"error": f"Error calculating Quick Ratio: {str(e)}"}

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
