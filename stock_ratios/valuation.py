import yfinance as yf
from config.valuation.valuation_config import (
    INDUSTRY_PE_BENCHMARKS, 
    DEFAULT_PE_BENCHMARK, 
    INDUSTRY_PB_BENCHMARK,
    INDUSTRY_PS_BENCHMARK,
    INDUSTRY_PEG_BENCHMARK,
    INDUSTRY_DIVIDEND_YIELD_BENCHMARK,
    INDUSTRY_DIVIDEND_PAYOUT_RATIO_BENCHMARK
)

from utils.benchmark import (
    get_industry_benchmark
)

class ValuationRatios:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self.info = self.stock.info

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

    def _get_industry_benchmark(self, ratio_type):
        sector = self.info.get("sector")
        industry = self.info.get("industry")
        if ratio_type == "PE":
            return get_industry_benchmark(sector, industry, INDUSTRY_PE_BENCHMARKS, DEFAULT_PE_BENCHMARK)
        elif ratio_type == "PB":
            return get_industry_benchmark(sector, industry, INDUSTRY_PB_BENCHMARK, (1.5, 3.0))
        elif ratio_type == "PS":
            return get_industry_benchmark(sector, industry, INDUSTRY_PS_BENCHMARK, (2.0, 4.0))
        elif ratio_type == "PEG":
            return get_industry_benchmark(sector, industry, INDUSTRY_PEG_BENCHMARK, (1.0, 1.2))
        elif ratio_type == "Dividend Yield":
            return get_industry_benchmark(sector, industry, INDUSTRY_DIVIDEND_YIELD_BENCHMARK, (2.0, 3.0))
        elif ratio_type == "Dividend Payout":
            return get_industry_benchmark(sector, industry, INDUSTRY_DIVIDEND_PAYOUT_RATIO_BENCHMARK, (30, 50))
        else:
            return None

    def _compare_to_benchmark(self, value, benchmark_range):
        if value is None or benchmark_range is None:
            return "Data Unavailable"
        try:
            lower_bound, upper_bound = benchmark_range
        except TypeError: #Handle the case where benchmark_range is not a tuple
            return "Data Unavailable"

        if value > upper_bound:
            return "Above Benchmark"
        elif value < lower_bound:
            return "Below Benchmark"
        else:
            return "Within Benchmark"
    
    def get_dividend_payout_ratio(self):
        try:
            # Fetch the dividend payout ratio from the Yahoo Finance info object
            dividend_payout_ratio = self.info.get("payoutRatio", None)

            if dividend_payout_ratio is None:
                return {"error": "Dividend Payout Ratio data is unavailable for this stock."}

            # Get the industry Dividend Payout Ratio Benchmark
            benchmark_range = self._get_industry_benchmark("Dividend Payout")
            comparison = self._compare_to_benchmark(dividend_payout_ratio * 100, benchmark_range)
            recommendation = self._get_recommendation_by_range(dividend_payout_ratio * 100, benchmark_range, buy_if_below=False)
            
            # Comparing Dividend Payout Ratio with the industry benchmark
            return {
                "dividend_payout_ratio": f"{round(dividend_payout_ratio * 100, 2)}%",
                "industry_dividend_payout_ratio_benchmark": benchmark_range,
                "dividend_payout_ratio_comparison": comparison,
                "recommendation": recommendation,
            }
        except KeyError:
            return {"error": "Error retrieving data for the stock."}

    def get_dividend_yield(self):
        try:
            dividend_yield = self.info.get("dividendYield", None)
            if dividend_yield is None:
                return {"error": "Dividend Yield data is unavailable for this stock."}

            benchmark_range = self._get_industry_benchmark("Dividend Yield")
            comparison = self._compare_to_benchmark(dividend_yield * 100, benchmark_range)
            recommendation = self._get_recommendation_by_range(dividend_yield * 100, benchmark_range, buy_if_below=False)

            return {
                "dividend_yield": f"{round(dividend_yield * 100, 2)}%",
                "industry_dividend_yield_benchmark": benchmark_range,
                "dividend_yield_comparison": comparison,
                "recommendation": recommendation,
            }
        except KeyError:
            return {"error": "Error retrieving data for the stock."}

        
    def get_peg_ratio(self):
        try:
            pe_ratio = self.info.get("trailingPE", None)
            earnings_growth = self.info.get("earningsQuarterlyGrowth", None)

            if pe_ratio is None or earnings_growth is None or earnings_growth == 0:
                return {"peg_ratio": None, "industry_peg_benchmark": None, "peg_comparison": "Data Unavailable", "recommendation": "Data Unavailable"}
            
            peg_ratio = pe_ratio / earnings_growth

            benchmark_range = self._get_industry_benchmark("PEG")
            comparison = self._compare_to_benchmark(peg_ratio, benchmark_range)
            recommendation = self._get_recommendation_by_range(peg_ratio, benchmark_range)

            return {
                "peg_ratio": peg_ratio,
                "industry_peg_benchmark": benchmark_range,
                "peg_comparison": comparison,
                "recommendation": recommendation,
            }
        except (KeyError, ZeroDivisionError):
            return {"peg_ratio": None, "industry_peg_benchmark": None, "peg_comparison": "Error in calculation", "recommendation": "Error in calculation"}
    

    def get_ps_ratio(self):
        try:
            ps_ratio = self.info.get("priceToSalesTrailing12Months", None)
            if ps_ratio is None:
                return {"error": "P/S ratio data is unavailable for this stock."}

            benchmark_range = self._get_industry_benchmark("PS")
            comparison = self._compare_to_benchmark(ps_ratio, benchmark_range)
            recommendation = self._get_recommendation_by_range(ps_ratio, benchmark_range)

            return {
                "ps_ratio": ps_ratio,
                "industry_ps_benchmark": benchmark_range,
                "ps_comparison": comparison,
                "recommendation": recommendation,
            }
        except KeyError:
            return {"error": "Error retrieving data for the stock."}
    
    
    def get_pe_ratio(self):
        try:
            trailing_pe = self.info.get("trailingPE")
            forward_pe = self.info.get("forwardPE")

            # Handle the case where benchmark range is not a tuple
            benchmark_range = self._get_industry_benchmark("PE")
            # print(f"***{benchmark_range}**")
            try:
                lower_bound, upper_bound = benchmark_range
            except TypeError:
                # If benchmark_range is not a tuple (e.g., integer), set it to None
                benchmark_range = None

            trailing_comparison = self._compare_to_benchmark(trailing_pe, benchmark_range)
            forward_comparison = self._compare_to_benchmark(forward_pe, benchmark_range)
            
            recommendation = "Hold" # Default
            if forward_pe is not None and forward_pe < lower_bound:
                recommendation = "Buy"
            elif trailing_pe is not None and trailing_pe < lower_bound:
                recommendation = "Buy"
            elif (forward_pe is not None and forward_pe > upper_bound) or (trailing_pe is not None and trailing_pe > upper_bound):
                recommendation = "Sell"
            elif trailing_pe is None and forward_pe is None:
                recommendation = "Insufficient data for recommendation"

            return {
                "trailing_pe": trailing_pe,
                "forward_pe": forward_pe,
                "industry_pe_benchmark": benchmark_range,
                "trailing_pe_comparison": trailing_comparison,
                "forward_pe_comparison": forward_comparison,
                "recommendation": recommendation
            }
        except Exception as e:
            return {"error": str(e)}
        
          
    def get_pb_ratio(self):
        try:
            # Fetching the P/B ratio directly from the Yahoo Finance info object
            pb_ratio = self.info.get("priceToBook", None)
            
            if pb_ratio is None:
                return {"error": "P/B ratio data is unavailable for this stock."}
            
            benchmark_range = self._get_industry_benchmark("PB")
            comparison = self._compare_to_benchmark(pb_ratio, benchmark_range)
            recommendation = self._get_recommendation_by_range(pb_ratio, benchmark_range)

            return {
                "pb_ratio": pb_ratio,
                "industry_pb_benchmark": benchmark_range,
                "pb_comparison": comparison,
                "recommendation": recommendation,
            }
        except KeyError:
            return {"error": "Error retrieving data for the stock."}

    def fetch_all_ratios(self):
        return {
            "P/E Ratio": self.get_pe_ratio(),
            "P/B Ratio": self.get_pb_ratio(),
            "P/S Ratio": self.get_ps_ratio(),
            "PEG Ratio": self.get_peg_ratio(),
            "Dividend Yield": self.get_dividend_yield(),
            "Dividend Payout": self.get_dividend_payout_ratio()
        }

