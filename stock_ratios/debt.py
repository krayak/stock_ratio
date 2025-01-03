import yfinance as yf
import math
from config.debt.debt_config import (
    INDUSTRY_DEBT_TO_EQUITY_RATIO_BENCHMARK,
    INDUSTRY_INTEREST_COVERAGE_RATIO_BENCHMARK,
    DEFAULT_DEBT_TO_EQUITY_RATIO_BENCHMARK,
    DEFAULT_INTEREST_COVERAGE_RATIO_BENCHMARK
)
from utils.benchmark import (
    get_industry_benchmark
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
        # print(f"Balance Sheet Keys for {ticker}: {self.balance_sheet.index.tolist()}")
        self.financials = self.stock.financials

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
        if ratio_type == "Debt-to-Equity Ratio":
            return get_industry_benchmark(sector, industry, INDUSTRY_DEBT_TO_EQUITY_RATIO_BENCHMARK, DEFAULT_DEBT_TO_EQUITY_RATIO_BENCHMARK)
        elif ratio_type == "Interest Coverage Ratio":
            return get_industry_benchmark(sector, industry, INDUSTRY_INTEREST_COVERAGE_RATIO_BENCHMARK, DEFAULT_INTEREST_COVERAGE_RATIO_BENCHMARK)
        else:
            return None

    def _get_financial_data(self, statement, keys):
        """
        Generic function to get financial data given a list of possible keys.
        """
        if statement is None or statement.empty:
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

    def get_total_debt(self):
        """Fetch the latest Total Debt."""
        possible_keys = ['Total Debt', 'Net Debt','totalDebt', 'Total Liabilities Net Minority Interest', 'Total Liabilities','totalLiabilities', 'Liabilities', 'Long Term Debt And Capital Lease Obligation', 'Long Term Debt', 'Current Debt And Capital Lease Obligation', 'Current Debt']
        return self._get_financial_data(self.balance_sheet, possible_keys)

    def get_total_equity(self):
        """Fetch the latest Total Equity."""
        possible_keys = ['Total Equity Gross Minority Interest', 'Stockholders Equity', 'Common Stock Equity', 'Total Equity', 'totalEquity', "Stockholders' Equity", "stockholdersEquity", "Equity"]
        equity = self._get_financial_data(self.balance_sheet, possible_keys)
        if equity is None:  # Try calculating if not found directly
            total_assets = self._get_financial_data(self.balance_sheet, ['Total Assets', 'totalAssets', 'Assets'])
            total_liabilities = self._get_financial_data(self.balance_sheet, ['Total Liabilities Net Minority Interest','Total Liabilities', 'totalLiabilities', 'Liabilities'])

            if total_assets is not None and total_liabilities is not None:
                equity = total_assets - total_liabilities
        return equity

    def get_ebit(self):
        """Fetch the latest EBIT (Earnings Before Interest and Taxes)."""
        possible_keys = ['EBIT', 'ebit', 'Operating Income', 'operatingIncome']
        ebit = self._get_financial_data(self.financials, possible_keys)
        if ebit is None:
            operating_income_keys = ['Operating Income', 'operatingIncome']
            operating_income = self._get_financial_data(self.financials, operating_income_keys)
            interest_expense_keys = ['Interest Expense', 'interestExpense']
            interest_expense = self._get_financial_data(self.financials, interest_expense_keys)
            if operating_income is not None and interest_expense is not None:
                ebit = operating_income + interest_expense
        return ebit

    def get_interest_expense(self):
        """Fetch the latest Interest Expense."""
        possible_keys = ['Interest Expense', 'interestExpense', 'Interest and Debt Expense', 'interestAndDebtExpense']
        return self._get_financial_data(self.financials, possible_keys)

    def calculate_debt_to_equity_ratio(self):
        """Calculate and evaluate Debt-to-Equity Ratio."""
        try:
            total_debt = self.get_total_debt()
            total_equity = self.get_total_equity()

            if total_debt is None:
                return {"Debt-to-Equity Ratio": None, "Industry Benchmark": None, "Comparison": "Total Debt Data Unavailable", "Recommendation": "Total Debt Data Unavailable"}
            if total_equity is None:
                return {"Debt-to-Equity Ratio": None, "Industry Benchmark": None, "Comparison": "Total Equity Data Unavailable", "Recommendation": "Total Equity Data Unavailable"}
            if total_equity == 0:
                return {"Debt-to-Equity Ratio": None, "Industry Benchmark": None, "Comparison": "Cannot calculate Debt-to-Equity Ratio, Total Equity is zero", "Recommendation": "Cannot calculate Debt-to-Equity Ratio, Total Equity is zero"}

            debt_to_equity_ratio = self._calculate_ratio(total_debt, total_equity)
            benchmark_range = self._get_benchmark("Debt-to-Equity Ratio")
            comparison = self._compare_to_benchmark(debt_to_equity_ratio, benchmark_range)
            recommendation = self._get_recommendation_by_range(debt_to_equity_ratio, benchmark_range, buy_if_below=True) #buy_if_below = True is important here

            return {
                "Debt-to-Equity Ratio": round(debt_to_equity_ratio, 2) if debt_to_equity_ratio is not None else None,
                "Industry Benchmark": benchmark_range,
                "Comparison": comparison,
                "Recommendation": recommendation
            }
        except Exception as e:
            return {"Debt-to-Equity Ratio": None, "Industry Benchmark": None, "Comparison": f"Error calculating Debt-to-Equity Ratio: {str(e)}", "Recommendation": f"Error calculating Debt-to-Equity Ratio: {str(e)}"}

    def calculate_interest_coverage_ratio(self):
        """Calculate and evaluate Interest Coverage Ratio."""
        try:
            ebit = self.get_ebit()
            interest_expense = self.get_interest_expense()

            if ebit is None:
                return {"Interest Coverage Ratio": None, "Industry Benchmark": None, "Comparison": "EBIT Data Unavailable", "Recommendation": "EBIT Data Unavailable"}
            if interest_expense is None:
                return {"Interest Coverage Ratio": None, "Industry Benchmark": None, "Comparison": "Interest Expense Data Unavailable", "Recommendation": "Interest Expense Data Unavailable"}
            if interest_expense == 0:
                return {"Interest Coverage Ratio": None, "Industry Benchmark": None, "Comparison": "Cannot calculate Interest Coverage Ratio, Interest Expense is zero", "Recommendation": "Cannot calculate Interest Coverage Ratio, Interest Expense is zero"}

            interest_coverage_ratio = self._calculate_ratio(ebit, interest_expense)
            benchmark_range = self._get_benchmark("Interest Coverage Ratio")
            comparison = self._compare_to_benchmark(interest_coverage_ratio, benchmark_range)
            recommendation = self._get_recommendation_by_range(interest_coverage_ratio, benchmark_range, buy_if_below=False) #buy_if_below=False is important here

            return {
                "Interest Coverage Ratio": round(interest_coverage_ratio, 2) if interest_coverage_ratio is not None else None,
                "Industry Benchmark": benchmark_range,
                "Comparison": comparison,
                "Recommendation": recommendation
            }
        except Exception as e:
            return {"Interest Coverage Ratio": None, "Industry Benchmark": None, "Comparison": f"Error calculating Interest Coverage Ratio: {str(e)}", "Recommendation": f"Error calculating Interest Coverage Ratio: {str(e)}"}

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
