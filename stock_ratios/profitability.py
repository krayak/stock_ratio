import yfinance as yf
import math
from config.profit.profitability_config import (
    INDUSTRY_ROA_BENCHMARK,
    INDUSTRY_ROE_BENCHMARK,
    INDUSTRY_PROFIT_MARGIN_BENCHMARK,
    INDUSTRY_GROSS_PROFIT_MARGIN_BENCHMARK,
    INDUSTRY_OPERATING_PROFIT_MARGIN_BENCHMARK,
    DEFAULT_ROA_BENCHMARK,
    DEFAULT_ROE_BENCHMARK,
    DEFAULT_PROFIT_MARGIN_BENCHMARK,
    DEFAULT_GROSS_PROFIT_MARGIN_BENCHMARK,
    DEFAULT_OPERATING_PROFIT_MARGIN_BENCHMARK
)
from utils.benchmark import (
    get_industry_benchmark
)

class ProfitabilityRatios:
    def __init__(self, ticker):
        """
        Initialize with the stock ticker and fetch relevant financial data.
        """
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self.info = self.stock.info
        self.income_statement = self.stock.financials
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
        if ratio_type == "ROA":
            return get_industry_benchmark(sector, industry, INDUSTRY_ROA_BENCHMARK, DEFAULT_ROA_BENCHMARK)
        elif ratio_type == "ROE":
            return get_industry_benchmark(sector, industry, INDUSTRY_ROE_BENCHMARK, DEFAULT_ROE_BENCHMARK)
        elif ratio_type == "Net Profit Margin":
            return get_industry_benchmark(sector, industry, INDUSTRY_PROFIT_MARGIN_BENCHMARK, DEFAULT_PROFIT_MARGIN_BENCHMARK)
        elif ratio_type == "Gross Profit Margin":
            return get_industry_benchmark(sector, industry, INDUSTRY_GROSS_PROFIT_MARGIN_BENCHMARK, DEFAULT_GROSS_PROFIT_MARGIN_BENCHMARK)
        elif ratio_type == "Operating Profit Margin":
            return get_industry_benchmark(sector, industry, INDUSTRY_OPERATING_PROFIT_MARGIN_BENCHMARK, DEFAULT_OPERATING_PROFIT_MARGIN_BENCHMARK)
        else:
            return None

    def get_net_profit(self):
        try:
            return self.income_statement.loc['Net Income'].iloc[0]
        except (KeyError, IndexError):
            return None
        
    def get_revenue(self):
        try:
            return self.income_statement.loc['Total Revenue'].iloc[0]
        except (KeyError, IndexError):
            return None

    def get_gross_profit(self):
        try:
            return self.income_statement.loc['Gross Profit'].iloc[0]
        except (KeyError, IndexError):
            return None

    def get_equity(self):
        possible_equity_lines = [
            "Total Stockholder Equity",
            "Total Equity Gross Minority Interest",
            "Stockholders Equity",  # Add other common variations
            "Equity",
            "Total Common Equity"
        ]
        # print("Balance Sheet Index:", self.balance_sheet.index) # Print the index for debugging

        try:
            for equity_line in possible_equity_lines:
                if equity_line in self.balance_sheet.index:
                    equity_value = self.balance_sheet.loc[equity_line].iloc[0]
                    print(f"Using equity line: {equity_line} with value {equity_value}")
                    return equity_value
            return None  # No suitable equity line found
        except (KeyError, IndexError):
            return None

    def get_total_assets(self):
        try:
            return self.balance_sheet.loc['Total Assets'].iloc[0]
        except (KeyError, IndexError):
            return None

    def _calculate_ratio(self, numerator, denominator):
        if numerator is None or denominator is None or denominator == 0:
            return None
        return (numerator / denominator) * 100

    def calculate_roa(self):
        """Calculate Return on Assets (ROA) using average total assets and provide recommendations."""
        try:
            # Fetch Net Income and Total Assets
            net_profit = self.get_net_profit()
            total_assets_end = self.get_total_assets()  # End-of-year total assets
            if net_profit is None or total_assets_end is None:
                return {"ROA (%)": None, "Industry Benchmark (%)": None, "Comparison": "Data Unavailable", "Recommendation": "Data Unavailable"}
        
            # Calculate Average Total Assets if historical data is available
            total_assets_start = (
                self.balance_sheet.loc['Total Assets'].iloc[1]
                if len(self.balance_sheet.loc['Total Assets']) > 1
                else total_assets_end  # Use end value if start not available
            )

            avg_total_assets = (total_assets_end + total_assets_start) / 2

            if avg_total_assets == 0:
                return {"ROA (%)": None, "Industry Benchmark (%)": None, "Comparison": "Cannot calculate ROA, Avg Total Assets is zero", "Recommendation": "Cannot calculate ROA, Avg Total Assets is zero"}

            # Calculate ROA
            roa = self._calculate_ratio(net_profit, avg_total_assets)
            benchmark_range = self._get_benchmark("ROA")
            comparison = self._compare_to_benchmark(roa, benchmark_range)
            recommendation = self._get_recommendation_by_range(roa, benchmark_range)

            return {
                "ROA (%)": round(roa, 2) if roa is not None else None,
                "Industry Benchmark (%)": benchmark_range,
                "Comparison": comparison,
                "Recommendation": recommendation
            }
        except (KeyError, IndexError) as e:
            return {"ROA (%)": None, "Industry Benchmark (%)": None, "Comparison": f"Error calculating ROA: {str(e)}", "Recommendation": f"Error calculating ROA: {str(e)}"}


    def calculate_roe(self):
        """Calculate and evaluate Return on Equity (ROE)."""
        try:
            net_profit = self.get_net_profit()
            equity = self.get_equity()

            # print("Balance Sheet:\n", self.balance_sheet)  # Debugging
            # print("Income Statement:\n", self.income_statement)  # Debugging
            # print(f"Net Profit: {net_profit}")
            # print(f"Equity: {equity}")

            if net_profit is None:
                return {"ROE (%)": None, "Industry Benchmark (%)": None, "Comparison": "Net Profit Data Unavailable", "Recommendation": "Net Profit Data Unavailable"}
            if equity is None:
                return {"ROE (%)": None, "Industry Benchmark (%)": None, "Comparison": "Equity Data Unavailable", "Recommendation": "Equity Data Unavailable"}
        
            if math.isnan(net_profit) or math.isnan(equity):
                return {"ROE (%)": None, "Industry Benchmark (%)": None, "Comparison": "Net Profit or Equity is NaN", "Recommendation": "Net Profit or Equity is NaN"}

            try:
                net_profit = float(net_profit)
                equity = float(equity)
            except (ValueError, TypeError):
                return {"ROE (%)": None, "Industry Benchmark (%)": None, "Comparison": "Invalid Data Type for Calculation", "Recommendation": "Invalid Data Type for Calculation"}
        
            if equity <= 0:  # Check for zero or negative equity
                print("WARNING: Equity is zero or negative. ROE cannot be meaningfully calculated.")
                return {"ROE (%)": None, "Industry Benchmark (%)": None, "Comparison": "Cannot calculate ROE, Equity is zero or negative", "Recommendation": "Cannot calculate ROE, Equity is zero or negative"}

            roe = self._calculate_ratio(net_profit, equity)
            benchmark_range = self._get_benchmark("ROE")
            comparison = self._compare_to_benchmark(roe, benchmark_range)
            recommendation = self._get_recommendation_by_range(roe, benchmark_range)

            return {
                "ROE (%)": round(roe, 2) if roe is not None else None,
                "Industry Benchmark (%)": benchmark_range,
                "Comparison": comparison,
                "Recommendation": recommendation
            }
        except Exception as e:
            return {"ROE (%)": None, "Industry Benchmark (%)": None, "Comparison": f"Error calculating ROE: {str(e)}", "Recommendation": f"Error calculating ROE: {str(e)}"}

    def calculate_net_profit_margin(self):
        """Calculate and evaluate Net Profit Margin (NPM)."""
        try:
            net_profit = self.get_net_profit()
            revenue = self.get_revenue()

            if net_profit is None or revenue is None:
                return {"Net Profit Margin (%)": None, "Industry Benchmark (%)": None, "Comparison": "Data Unavailable", "Recommendation": "Data Unavailable"}
            
            npm = self._calculate_ratio(net_profit, revenue)
            benchmark_range = self._get_benchmark("Net Profit Margin")
            comparison = self._compare_to_benchmark(npm, benchmark_range)
            recommendation = self._get_recommendation_by_range(npm, benchmark_range)

            return {
                "Net Profit Margin (%)": round(npm, 2) if npm is not None else None,
                "Industry Benchmark (%)": benchmark_range,
                "Comparison": comparison,
                "Recommendation": recommendation
            }
        except Exception as e:
            return {"error": f"Error calculating Net Profit Margin: {str(e)}"}

    def calculate_gross_profit_margin(self):
        """Calculate and evaluate Gross Profit Margin (GPM)."""
        try:
            gross_profit = self.get_gross_profit()
            revenue = self.get_revenue()

            if gross_profit is None or revenue is None:
                return {"Gross Profit Margin (%)": None, "Industry Benchmark (%)": None, "Comparison": "Data Unavailable", "Recommendation": "Data Unavailable"}

            gpm = self._calculate_ratio(gross_profit, revenue)
            benchmark_range = self._get_benchmark("Gross Profit Margin")

            comparison = self._compare_to_benchmark(gpm, benchmark_range)
            recommendation = self._get_recommendation_by_range(gpm, benchmark_range)

            return {
                "Gross Profit Margin (%)": round(gpm, 2) if gpm is not None else None,
                "Industry Benchmark (%)": benchmark_range,
                "Comparison": comparison,
                "Recommendation": recommendation
            }
        except (KeyError, IndexError, ZeroDivisionError) as e: #Added ZeroDivisionError
            return {"Gross Profit Margin (%)": None, "Industry Benchmark (%)": None, "Comparison": f"Error calculating Gross Profit Margin: {str(e)}", "Recommendation": f"Error calculating Gross Profit Margin: {str(e)}"}


    def fetch_all_ratios(self):
        """Fetch and return all profitability ratios with benchmarks and recommendations."""
        ratios = {
            "ROA": self.calculate_roa,
            "ROE": self.calculate_roe,
            "Net Profit Margin": self.calculate_net_profit_margin,
            "Gross Profit Margin": self.calculate_gross_profit_margin,
        }
        results = {}
        for ratio_name, calculation_method in ratios.items():
            results[ratio_name] = calculation_method()
        return results
