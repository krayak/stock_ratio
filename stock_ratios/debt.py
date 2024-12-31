import yfinance as yf
from utils.debt_helper import (
    get_industry_debt_to_equity_benchmark,
    get_industry_interest_coverage_benchmark,
)


class DebtRatios:
    def __init__(self, ticker):
        """
        Initialize with the stock ticker and fetch relevant financial data.
        """
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self.info = self.stock.info
        self.balance_sheet = self.stock.balance_sheet
        self.financials = self.stock.financials

    def _get_benchmark(self, ratio_name):
        """
        Fetch the industry benchmark for a given ratio.
        """
        benchmark_functions = {
            "Debt-to-Equity Ratio": get_industry_debt_to_equity_benchmark,
            "Interest Coverage Ratio": get_industry_interest_coverage_benchmark,
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

    def _get_recommendation(self, ratio, benchmark, comparison_type="higher"):
        """
        Generate a recommendation based on the comparison of the ratio to the industry benchmark.
        """
        if ratio is None or benchmark is None:
            return "Data Unavailable"
        elif comparison_type == "higher" and ratio > benchmark:
            return "Above Benchmark - Positive"
        elif comparison_type == "lower" and ratio < benchmark:
            return "Below Benchmark - Positive"
        elif ratio == benchmark:
            return "At Benchmark - Neutral"
        else:
            return "Below Benchmark - Negative" if comparison_type == "higher" else "Above Benchmark - Negative"

    def get_total_debt(self):
        """Fetch the latest Total Debt."""
        return self._get_latest_financial_value(self.balance_sheet, 'Total Debt')

    def get_total_equity(self):
        """Fetch the latest Total Equity."""
        return self._get_latest_financial_value(self.balance_sheet, 'Total Equity')

    def get_ebit(self):
        """Fetch the latest EBIT (Earnings Before Interest and Taxes)."""
        return self._get_latest_financial_value(self.financials, 'EBIT')

    def get_interest_expense(self):
        """Fetch the latest Interest Expense."""
        return self._get_latest_financial_value(self.financials, 'Interest Expense')

    def calculate_debt_to_equity_ratio(self):
        """Calculate and evaluate Debt-to-Equity Ratio."""
        try:
            total_debt = self.get_total_debt()
            total_equity = self.get_total_equity()

            # Calculate Debt-to-Equity Ratio
            debt_to_equity_ratio = self._calculate_ratio(total_debt, total_equity)
            debt_to_equity_benchmark = self._get_benchmark("Debt-to-Equity Ratio")
            recommendation = self._get_recommendation(debt_to_equity_ratio, debt_to_equity_benchmark, "lower")

            return {
                "Debt-to-Equity Ratio": round(debt_to_equity_ratio, 2) if debt_to_equity_ratio is not None else "N/A",
                "Industry Benchmark": round(debt_to_equity_benchmark, 2) if debt_to_equity_benchmark else "N/A",
                "Comparison": (
                    "Above Benchmark" if debt_to_equity_ratio is not None and debt_to_equity_ratio > debt_to_equity_benchmark else
                    "Below Benchmark" if debt_to_equity_ratio is not None and debt_to_equity_ratio < debt_to_equity_benchmark else
                    "At Benchmark" if debt_to_equity_ratio is not None and debt_to_equity_ratio == debt_to_equity_benchmark else
                    "Benchmark Unavailable"
                ),
                "Recommendation": recommendation
            }
        except Exception as e:
            return {"error": f"Error calculating Debt-to-Equity Ratio: {str(e)}"}

    def calculate_interest_coverage_ratio(self):
        """Calculate and evaluate Interest Coverage Ratio."""
        try:
            ebit = self.get_ebit()
            interest_expense = self.get_interest_expense()

            # Calculate Interest Coverage Ratio
            interest_coverage_ratio = self._calculate_ratio(ebit, interest_expense)
            interest_coverage_benchmark = self._get_benchmark("Interest Coverage Ratio")
            recommendation = self._get_recommendation(interest_coverage_ratio, interest_coverage_benchmark, "higher")

            return {
                "Interest Coverage Ratio": round(interest_coverage_ratio, 2) if interest_coverage_ratio is not None else "N/A",
                "Industry Benchmark": round(interest_coverage_benchmark, 2) if interest_coverage_benchmark else "N/A",
                "Comparison": (
                    "Above Benchmark" if interest_coverage_ratio is not None and interest_coverage_ratio > interest_coverage_benchmark else
                    "Below Benchmark" if interest_coverage_ratio is not None and interest_coverage_ratio < interest_coverage_benchmark else
                    "At Benchmark" if interest_coverage_ratio is not None and interest_coverage_ratio == interest_coverage_benchmark else
                    "Benchmark Unavailable"
                ),
                "Recommendation": recommendation
            }
        except Exception as e:
            return {"error": f"Error calculating Interest Coverage Ratio: {str(e)}"}

    def fetch_all_ratios(self):
        """Fetch and return all debt ratios with benchmarks and recommendations."""
        ratios = {
            "Debt-to-Equity Ratio": self.calculate_debt_to_equity_ratio,
            "Interest Coverage Ratio": self.calculate_interest_coverage_ratio,
        }
        results = {}
        for ratio_name, calculation_method in ratios.items():
            results[ratio_name] = calculation_method()  # Call each calculation method
        return results
