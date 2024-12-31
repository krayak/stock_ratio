import yfinance as yf
from utils.efficiency_helper import (
    get_industry_asset_turnover_benchmark,
    get_industry_inventory_turnover_benchmark
)


class EfficiencyRatios:
    def __init__(self, ticker):
        """
        Initialize with the stock ticker and fetch relevant financial data.
        """
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self.info = self.stock.info
        self.financials = self.stock.financials
        self.balance_sheet = self.stock.balance_sheet

    def _get_benchmark(self, ratio_name):
        """
        Fetch the industry benchmark for a given ratio.
        """
        benchmark_functions = {
            "Asset Turnover Ratio": get_industry_asset_turnover_benchmark,
            "Inventory Turnover Ratio": get_industry_inventory_turnover_benchmark,
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

    def get_total_revenue(self):
        """Fetch the latest Total Revenue."""
        return self._get_latest_financial_value(self.financials, 'Total Revenue')

    def get_total_assets(self):
        """Fetch the latest Total Assets."""
        return self._get_latest_financial_value(self.balance_sheet, 'Total Assets')

    def get_cost_of_goods_sold(self):
        """Fetch the latest Cost of Goods Sold (COGS)."""
        return self._get_latest_financial_value(self.financials, 'Cost of Revenue')

    def get_inventory(self):
        """Fetch the latest Inventory value."""
        return self._get_latest_financial_value(self.balance_sheet, 'Inventory')

    def calculate_asset_turnover_ratio(self):
        """Calculate and evaluate Asset Turnover Ratio."""
        try:
            total_revenue = self.get_total_revenue()
            total_assets = self.get_total_assets()

            # Calculate Asset Turnover Ratio
            asset_turnover_ratio = self._calculate_ratio(total_revenue, total_assets)
            asset_turnover_benchmark = self._get_benchmark("Asset Turnover Ratio")
            recommendation = self._get_recommendation(asset_turnover_ratio, asset_turnover_benchmark)

            return {
                "Asset Turnover Ratio": round(asset_turnover_ratio, 2) if asset_turnover_ratio is not None else "N/A",
                "Industry Benchmark": round(asset_turnover_benchmark, 2) if asset_turnover_benchmark else "N/A",
                "Comparison": (
                    "Above Benchmark" if asset_turnover_ratio is not None and asset_turnover_ratio > asset_turnover_benchmark else
                    "Below Benchmark" if asset_turnover_ratio is not None and asset_turnover_ratio < asset_turnover_benchmark else
                    "At Benchmark" if asset_turnover_ratio is not None and asset_turnover_ratio == asset_turnover_benchmark else
                    "Benchmark Unavailable"
                ),
                "Recommendation": recommendation
            }
        except Exception as e:
            return {"error": f"Error calculating Asset Turnover Ratio: {str(e)}"}

    def calculate_inventory_turnover_ratio(self):
        """Calculate and evaluate Inventory Turnover Ratio."""
        try:
            cogs = self.get_cost_of_goods_sold()
            inventory = self.get_inventory()

            # Calculate Inventory Turnover Ratio
            inventory_turnover_ratio = self._calculate_ratio(cogs, inventory)
            inventory_turnover_benchmark = self._get_benchmark("Inventory Turnover Ratio")
            recommendation = self._get_recommendation(inventory_turnover_ratio, inventory_turnover_benchmark)

            return {
                "Inventory Turnover Ratio": round(inventory_turnover_ratio, 2) if inventory_turnover_ratio is not None else "N/A",
                "Industry Benchmark": round(inventory_turnover_benchmark, 2) if inventory_turnover_benchmark else "N/A",
                "Comparison": (
                    "Above Benchmark" if inventory_turnover_ratio is not None and inventory_turnover_ratio > inventory_turnover_benchmark else
                    "Below Benchmark" if inventory_turnover_ratio is not None and inventory_turnover_ratio < inventory_turnover_benchmark else
                    "At Benchmark" if inventory_turnover_ratio is not None and inventory_turnover_ratio == inventory_turnover_benchmark else
                    "Benchmark Unavailable"
                ),
                "Recommendation": recommendation
            }
        except Exception as e:
            return {"error": f"Error calculating Inventory Turnover Ratio: {str(e)}"}

    def fetch_all_ratios(self):
        """Fetch and return all efficiency ratios with benchmarks and recommendations."""
        ratios = {
            "Asset Turnover Ratio": self.calculate_asset_turnover_ratio,
            "Inventory Turnover Ratio": self.calculate_inventory_turnover_ratio,
        }
        results = {}
        for ratio_name, calculation_method in ratios.items():
            results[ratio_name] = calculation_method()  # Call each calculation method
        return results
