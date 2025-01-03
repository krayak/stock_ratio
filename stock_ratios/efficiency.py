import yfinance as yf
import math
from config.efficiency.efficiency_config import (
    INDUSTRY_ASSET_TURNOVER_RATIO_BENCHMARK,
    INDUSTRY_INVENTORY_TURNOVER_RATIO_BENCHMARK,
    INDUSTRY_RECEIVABLES_TURNOVER_RATIO_BENCHMARK,
    DEFAULT_ASSET_TURNOVER_RATIO_BENCHMARK,
    DEFAULT_INVENTORY_TURNOVER_RATIO_BENCHMARK,
    DEFAULT_RECEIVABLES_TURNOVER_RATIO_BENCHMARK
)
from utils.benchmark import (
    get_industry_benchmark
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
        if ratio_type == "Asset Turnover Ratio":
            return get_industry_benchmark(sector, industry, INDUSTRY_ASSET_TURNOVER_RATIO_BENCHMARK, DEFAULT_ASSET_TURNOVER_RATIO_BENCHMARK)
        elif ratio_type == "Inventory Turnover Ratio":
            return get_industry_benchmark(sector, industry, INDUSTRY_INVENTORY_TURNOVER_RATIO_BENCHMARK, DEFAULT_INVENTORY_TURNOVER_RATIO_BENCHMARK)
        elif ratio_type == "Receivables Turnover Ratio":
            return get_industry_benchmark(sector, industry, INDUSTRY_RECEIVABLES_TURNOVER_RATIO_BENCHMARK, DEFAULT_RECEIVABLES_TURNOVER_RATIO_BENCHMARK)
        else:
            return None

    def _get_financial_data(self, statement, keys): # Added statement parameter
        """
        Generic function to get financial data given a list of possible keys.
        """
        if statement is None or statement.empty: #Check for empty statement
            return None
        for key in keys:
            try:
                value = statement.loc[key].iloc[0]
                if not (isinstance(value, (int, float)) and not math.isnan(value)):
                    continue  # Skip if value is not a valid number
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

    def get_total_revenue(self):
        """Fetch the latest Total Revenue."""
        return self._get_financial_data(self.financials, ['Total Revenue', 'totalRevenue'])

    def get_total_assets(self):
        """Fetch the latest Total Assets."""
        return self._get_financial_data(self.balance_sheet, ['Total Assets', 'totalAssets', 'Assets'])

    def get_cost_of_goods_sold(self):
        """Fetch the latest Cost of Goods Sold (COGS)."""
        possible_keys = ['Cost of Revenue', 'costOfRevenue', 'Cost Of Goods Sold', 'costOfGoodsSold']
        cogs = self._get_financial_data(self.financials, possible_keys)
        if cogs is None:  # Try calculating COGS if not directly available
            gross_profit_keys = ['Gross Profit', 'grossProfit']
            gross_profit = self._get_financial_data(self.financials, gross_profit_keys)
            revenue = self.get_total_revenue()
            if gross_profit is not None and revenue is not None:
                cogs = revenue - gross_profit  # COGS = Revenue - Gross Profit
        return cogs

    def get_inventory(self):
        """Fetch the latest Inventory value."""
        return self._get_financial_data(self.balance_sheet, ["Inventory", "inventory", "Inventories"])

    def calculate_asset_turnover_ratio(self):
        """Calculate and evaluate Asset Turnover Ratio."""
        try:
            total_revenue = self.get_total_revenue()
            total_assets_end = self.get_total_assets()

            # Check data availability early
            if total_revenue is None:
                return {"Asset Turnover Ratio": None, "Industry Benchmark": None, "Comparison": "Revenue Data Unavailable", "Recommendation": "Revenue Data Unavailable"}
            if total_assets_end is None:
                return {"Asset Turnover Ratio": None, "Industry Benchmark": None, "Comparison": "Assets Data Unavailable", "Recommendation": "Assets Data Unavailable"}

            total_assets_start = (
                self.balance_sheet.loc['Total Assets'].iloc[1] if 'Total Assets' in self.balance_sheet.index and len(self.balance_sheet.loc['Total Assets']) > 1 else total_assets_end
            )

            avg_total_assets = (total_assets_end + total_assets_start) / 2 if total_assets_start is not None and total_assets_end is not None else None

            if avg_total_assets is None or avg_total_assets == 0:
                return {"Asset Turnover Ratio": None, "Industry Benchmark": None, "Comparison": "Cannot calculate Asset Turnover Ratio, Avg Total Assets is zero or data unavailable", "Recommendation": "Cannot calculate Asset Turnover Ratio, Avg Total Assets is zero or data unavailable"}

            asset_turnover_ratio = self._calculate_ratio(total_revenue, avg_total_assets)
            benchmark_range = self._get_benchmark("Asset Turnover Ratio")
            comparison = self._compare_to_benchmark(asset_turnover_ratio, benchmark_range)
            recommendation = self._get_recommendation_by_range(asset_turnover_ratio, benchmark_range)

            return {
                "Asset Turnover Ratio": round(asset_turnover_ratio, 2) if asset_turnover_ratio is not None else None,
                "Industry Benchmark": benchmark_range,
                "Comparison": comparison,
                "Recommendation": recommendation
            }
        except Exception as e:
            return {"Asset Turnover Ratio": None, "Industry Benchmark": None, "Comparison": f"Error calculating Asset Turnover Ratio: {str(e)}", "Recommendation": f"Error calculating Asset Turnover Ratio: {str(e)}"}


    def calculate_inventory_turnover_ratio(self):
        """Calculate and evaluate Inventory Turnover Ratio."""
        try:
            cogs = self.get_cost_of_goods_sold()
            inventory_end = self.get_inventory()

            if cogs is None:
                return {"Inventory Turnover Ratio": None, "Industry Benchmark": None, "Comparison": "COGS Data Unavailable", "Recommendation": "COGS Data Unavailable"}
            if inventory_end is None:
                return {"Inventory Turnover Ratio": None, "Industry Benchmark": None, "Comparison": "Inventory Data Unavailable", "Recommendation": "Inventory Data Unavailable"}

            inventory_start = (
                self.balance_sheet.loc['Inventory'].iloc[1] if 'Inventory' in self.balance_sheet.index and len(self.balance_sheet.loc['Inventory']) > 1 else inventory_end
            )
            avg_inventory = (inventory_end + inventory_start) / 2 if inventory_end is not None and inventory_start is not None else None

            if avg_inventory is None or avg_inventory == 0:
                return {"Inventory Turnover Ratio": None, "Industry Benchmark": None, "Comparison": "Cannot calculate Inventory Turnover Ratio, Avg Inventory is zero or data unavailable", "Recommendation": "Cannot calculate Inventory Turnover Ratio, Avg Inventory is zero or data unavailable"}

            inventory_turnover_ratio = self._calculate_ratio(cogs, avg_inventory)
            benchmark_range = self._get_benchmark("Inventory Turnover Ratio")
            comparison = self._compare_to_benchmark(inventory_turnover_ratio, benchmark_range)
            recommendation = self._get_recommendation_by_range(inventory_turnover_ratio, benchmark_range)

            return {
                "Inventory Turnover Ratio": round(inventory_turnover_ratio, 2) if inventory_turnover_ratio is not None else None,
                "Industry Benchmark": benchmark_range,
                "Comparison": comparison,
                "Recommendation": recommendation
            }
        except Exception as e:
            return {"Inventory Turnover Ratio": None, "Industry Benchmark": None, "Comparison": f"Error calculating Inventory Turnover Ratio: {str(e)}", "Recommendation": f"Error calculating Inventory Turnover Ratio: {str(e)}"}


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
