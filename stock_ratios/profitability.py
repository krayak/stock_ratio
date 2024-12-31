import logging

logging.basicConfig(level=logging.INFO)

import yfinance as yf
from utils.profitability_helper import (
    get_industry_roa_benchmark,
    get_industry_roe_benchmark,
    get_industry_net_profit_margin_benchmark,
    get_industry_gross_profit_margin_benchmark
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

    def _get_benchmark(self, ratio_name):
        """
        Fetch the industry benchmark for a given ratio.
        """
        benchmark_functions = {
        "ROA": get_industry_roa_benchmark,
        "ROE": get_industry_roe_benchmark,
        "Net Profit Margin": get_industry_net_profit_margin_benchmark,
        "Gross Profit Margin": get_industry_gross_profit_margin_benchmark,
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
            logging.info(f"Key '{key}' not found in financial statement.")
            return None

    def _calculate_ratio(self, numerator, denominator):
        """
        Utility function to calculate a ratio and handle zero or None values.
        """
        if numerator is None or denominator is None or denominator == 0:
            return None
        return (numerator / denominator) * 100

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

    def get_net_profit(self):
        """Fetch the latest Net Income (Net Profit)."""
        return self._get_latest_financial_value(self.income_statement, 'Net Income')

    def get_revenue(self):
        """Fetch the latest Total Revenue."""
        return self._get_latest_financial_value(self.income_statement, 'Total Revenue')

    def get_operating_income(self):
        """Fetch the latest Operating Income (EBIT)."""
        return self._get_latest_financial_value(self.income_statement, 'Operating Income')

    def get_gross_profit(self):
        """Fetch the latest Gross Profit."""
        return self._get_latest_financial_value(self.income_statement, 'Gross Profit')

    def get_total_assets(self):
        """Fetch the latest Total Assets from the balance sheet."""
        return self._get_latest_financial_value(self.balance_sheet, 'Total Assets')

    def get_equity(self):
        """Fetch the latest Shareholder Equity from the balance sheet."""
        return self._get_latest_financial_value(self.balance_sheet, 'Total Stockholder Equity')

    def calculate_roa(self):
        """Calculate Return on Assets (ROA) using average total assets and provide recommendations."""
        try:
            # Fetch Net Income and Total Assets
            net_profit = self.get_net_profit()
            total_assets_end = self.get_total_assets()  # End-of-year total assets
        
            # Calculate Average Total Assets if historical data is available
            total_assets_start = (
                self.balance_sheet.loc['Total Assets'][1]
                if len(self.balance_sheet.loc['Total Assets']) > 1
                else total_assets_end  # Use end value if start not available
            )

            avg_total_assets = (total_assets_end + total_assets_start) / 2

            if avg_total_assets == 0:  # Avoid division by zero
                return {"error": "Average Total Assets is zero, cannot calculate ROA."}

            # Calculate ROA
            roa = (net_profit / avg_total_assets) * 100
            roa_benchmark = self._get_benchmark("ROA")
        
            # Compare with benchmark and provide recommendation
            recommendation = self._get_recommendation(roa, roa_benchmark)

            return {
                "ROA (%)": round(roa, 2),
                "Industry Benchmark (%)": round(roa_benchmark, 2) if roa_benchmark else "N/A",
                "Comparison": (
                    "Above Benchmark" if roa > roa_benchmark else
                    "Below Benchmark" if roa < roa_benchmark else
                    "At Benchmark" if roa == roa_benchmark else
                    "Benchmark Unavailable"
                ),
                "Recommendation": recommendation
            }
        except Exception as e:
            return {"error": f"Error calculating ROA: {str(e)}"}



    def calculate_roe(self):
        """Calculate and evaluate Return on Equity (ROE)."""
        try:
            net_profit = self.get_net_profit()
            equity = self.get_equity()

            if equity == 0:
                return {"error": "Shareholder Equity is zero, cannot calculate ROE."}

            roe = self._calculate_ratio(net_profit, equity)
            roe_benchmark = self._get_benchmark("ROE")
            recommendation = self._get_recommendation(roe, roe_benchmark)
        
            return {
                "ROE (%)": round(roe, 2) if roe is not None else "N/A",
                "Industry Benchmark (%)": round(roe_benchmark, 2) if roe_benchmark else "N/A",
                "Comparison": (
                    "Above Benchmark" if roe is not None and roe_benchmark is not None and roe > roe_benchmark else
                    "Below Benchmark" if roe is not None and roe_benchmark is not None and roe < roe_benchmark else
                    "At Benchmark" if roe is not None and roe_benchmark is not None and roe == roe_benchmark else
                    "Benchmark Unavailable"
                ),
                "Recommendation": recommendation
            }
        except Exception as e:
            return {"error": f"Error calculating ROE: {str(e)}"}

    def calculate_net_profit_margin(self):
        """Calculate and evaluate Net Profit Margin (NPM)."""
        try:
            net_profit = self.get_net_profit()
            revenue = self.get_revenue()

            # Handle cases where revenue is zero or None
            if revenue is None or revenue == 0:
                npm = None
            else:
                npm = (net_profit / revenue) * 100

            npm_benchmark = self._get_benchmark("Net Profit Margin")
            recommendation = self._get_recommendation(npm, npm_benchmark)

            return {
                "Net Profit Margin (%)": round(npm, 2) if npm is not None else "N/A",
                "Industry Benchmark (%)": round(npm_benchmark, 2) if npm_benchmark else "N/A",
                "Comparison": (
                    "Above Benchmark" if npm is not None and npm_benchmark is not None and npm > npm_benchmark else
                    "Below Benchmark" if npm is not None and npm_benchmark is not None and npm < npm_benchmark else
                    "At Benchmark" if npm is not None and npm_benchmark is not None and npm == npm_benchmark else
                    "Benchmark Unavailable"
                ),
                "Recommendation": recommendation
            }
        except Exception as e:
            return {"error": f"Error calculating Net Profit Margin: {str(e)}"}

    def calculate_gross_profit_margin(self):
        """Calculate and evaluate Gross Profit Margin (GPM)."""
        try:
            gross_profit = self.get_gross_profit()
            revenue = self.get_revenue()

            # Handle cases where revenue is zero or None
            if revenue is None or revenue == 0:
                gpm = None
            else:
                gpm = (gross_profit / revenue) * 100

            gpm_benchmark = self._get_benchmark("Gross Profit Margin")
            recommendation = self._get_recommendation(gpm, gpm_benchmark)

            return {
                "Gross Profit Margin (%)": round(gpm, 2) if gpm is not None else "N/A",
                "Industry Benchmark (%)": round(gpm_benchmark, 2) if gpm_benchmark else "N/A",
                "Comparison": (
                    "Above Benchmark" if gpm is not None and gpm_benchmark is not None and gpm > gpm_benchmark else
                    "Below Benchmark" if gpm is not None and gpm_benchmark is not None and gpm < gpm_benchmark else
                    "At Benchmark" if gpm is not None and gpm_benchmark is not None and gpm == gpm_benchmark else
                    "Benchmark Unavailable"
                ),
                "Recommendation": recommendation
            }
        except Exception as e:
            return {"error": f"Error calculating Gross Profit Margin: {str(e)}"}

    # def calculate_net_profit_margin(self):
    #     """Calculate Net Profit Margin (NPM)."""
    #     return self._calculate_ratio(self.get_net_profit(), self.get_revenue())

    # def calculate_operating_profit_margin(self):
    #     """Calculate Operating Profit Margin (OPM)."""
    #     return self._calculate_ratio(self.get_operating_income(), self.get_revenue())

    # def calculate_gross_profit_margin(self):
    #     """Calculate Gross Profit Margin (GPM)."""
    #     return self._calculate_ratio(self.get_gross_profit(), self.get_revenue())

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
            results[ratio_name] = calculation_method()  # Call each calculation method
        return results
