import yfinance as yf
from utils.valuation_helper import (
    get_industry_pe_benchmark,
    get_industry_pb_benchmark,
    get_industry_ps_benchmark,
    get_industry_peg_benchmark,
    get_industry_dividend_yield_benchmark,
    get_industry_dividend_payout_ratio_benchmark
)

class ValuationRatios:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self.info = self.stock.info
        self.industry_pe_benchmark = self._get_industry_pe_benchmark()

    def _get_div_payout_recommendation(self, dividend_payout_ratio, industry_benchmark):
        if dividend_payout_ratio > industry_benchmark:
            return "Buy"  # Buy if the stock's dividend payout ratio is above the benchmark
        elif dividend_payout_ratio < industry_benchmark:
            return "Sell"  # Sell if the stock's dividend payout ratio is below the benchmark
        else:
            return "Hold"  # Hold if it's exactly at the benchmark
    
    def get_dividend_payout_ratio(self):
        try:
            # Fetch the dividend payout ratio from the Yahoo Finance info object
            dividend_payout_ratio = self.info.get("payoutRatio", None)

            if dividend_payout_ratio is None:
                return {"error": "Dividend Payout Ratio data is unavailable for this stock."}

            # Get the industry Dividend Payout Ratio Benchmark
            industry = self.info.get("sector", "Unknown")
            industry_dividend_payout_ratio_benchmark = get_industry_dividend_payout_ratio_benchmark(industry)
            
            # Comparing Dividend Payout Ratio with the industry benchmark
            dividend_payout_ratio_comparison = (
                "Above Benchmark" if dividend_payout_ratio and industry_dividend_payout_ratio_benchmark and dividend_payout_ratio > industry_dividend_payout_ratio_benchmark else
                "Below Benchmark" if dividend_payout_ratio and industry_dividend_payout_ratio_benchmark and dividend_payout_ratio < industry_dividend_payout_ratio_benchmark else
                "At Benchmark" if dividend_payout_ratio and industry_dividend_payout_ratio_benchmark and dividend_payout_ratio == industry_dividend_payout_ratio_benchmark else
                "Data Unavailable"
            )
            
            # Return the data as a percentage value and compare with benchmark
            return {
                "dividend_payout_ratio": f"{round(dividend_payout_ratio * 100, 2)}%",  # Multiply by 100 to convert to percentage
                "industry_dividend_payout_ratio_benchmark": f"{round(industry_dividend_payout_ratio_benchmark, 2)}%",  # Add % here as well
                "dividend_payout_ratio_comparison": dividend_payout_ratio_comparison,
                "recommendation": self._get_div_payout_recommendation(dividend_payout_ratio, industry_dividend_payout_ratio_benchmark)
            }
        except KeyError:
            return {"error": "Error retrieving data for the stock."}

    def get_dividend_yield(self):
        try:
            # Fetching the dividend yield directly from the Yahoo Finance info object
            dividend_yield = self.info.get("dividendYield", None)

            if dividend_yield is None:
                return {"error": "Dividend Yield data is unavailable for this stock."}

            # Get the industry Dividend Yield Benchmark using the helper function
            industry = self.info.get("sector", "Unknown")
            industry_dividend_yield_benchmark = get_industry_dividend_yield_benchmark(industry)
            
            # Comparing Dividend Yield with the industry benchmark
            dividend_yield_comparison = (
                "Above Benchmark" if dividend_yield and industry_dividend_yield_benchmark and dividend_yield > industry_dividend_yield_benchmark else
                "Below Benchmark" if dividend_yield and industry_dividend_yield_benchmark and dividend_yield < industry_dividend_yield_benchmark else
                "At Benchmark" if dividend_yield and industry_dividend_yield_benchmark and dividend_yield == industry_dividend_yield_benchmark else
                "Data Unavailable"
            )
            
            # Return the data
            return {
                "dividend_yield": f"{round(dividend_yield * 100, 2)}",  # Multiply by 100 to convert into percentage
                "industry_dividend_yield_benchmark": industry_dividend_yield_benchmark,
                "dividend_yield_comparison": dividend_yield_comparison,
                "recommendation": self._get_div_yield_recommendation(dividend_yield, industry_dividend_yield_benchmark)
            }
        except KeyError:
            return {"error": "Error retrieving data for the stock."}

    def _get_div_yield_recommendation(self, dividend_yield, industry_dividend_yield_benchmark):
        if dividend_yield is None or industry_dividend_yield_benchmark is None:
            return "Data Unavailable"
        
        if dividend_yield > industry_dividend_yield_benchmark:
            return "Buy"
        elif dividend_yield < industry_dividend_yield_benchmark:
            return "Sell"
        else:
            return "Hold"
        
    def get_peg_ratio(self):
        try:
            # Fetching the P/E ratio and earnings growth rate directly from the Yahoo Finance info object
            pe_ratio = self.info.get("trailingPE", None)
            earnings_growth = self.info.get("earningsQuarterlyGrowth", None)

            if pe_ratio is None or earnings_growth is None:
                return {"error": "P/E ratio or Earnings Growth data is unavailable for this stock."}
            
            # Calculating PEG ratio
            peg_ratio = pe_ratio / earnings_growth

            # Get the industry PEG Benchmark using the helper function
            industry = self.info.get("sector", "Unknown")
            industry_peg_benchmark = get_industry_peg_benchmark(industry)
            
            # Comparing PEG ratio with the industry benchmark
            peg_comparison = (
                "Above Benchmark" if peg_ratio and industry_peg_benchmark and peg_ratio > industry_peg_benchmark else
                "Below Benchmark" if peg_ratio and industry_peg_benchmark and peg_ratio < industry_peg_benchmark else
                "At Benchmark" if peg_ratio and industry_peg_benchmark and peg_ratio == industry_peg_benchmark else
                "Data Unavailable"
            )
            
            # Return the data
            return {
                "peg_ratio": peg_ratio,
                "industry_peg_benchmark": industry_peg_benchmark,
                "peg_comparison": peg_comparison,
                "recommendation": self._get_ps_recommendation(peg_ratio, industry_peg_benchmark)
            }
        except KeyError:
            return {"error": "Error retrieving data for the stock."}
    
    def _get_peg_recommendation(self, peg_ratio, industry_peg_benchmark):
        if peg_ratio is None or industry_peg_benchmark is None:
            return "Data Unavailable"
        
        if peg_ratio > industry_peg_benchmark:
            return "Sell"
        elif peg_ratio < industry_peg_benchmark:
            return "Buy"
        else:
            return "Hold"

    def get_ps_ratio(self):
        try:
            # Fetching the P/S ratio directly from the Yahoo Finance info object
            ps_ratio = self.info.get("priceToSalesTrailing12Months", None)
            
            if ps_ratio is None:
                return {"error": "P/S ratio data is unavailable for this stock."}
            
            # Get the industry P/S Benchmark using the helper function
            industry = self.info.get("sector", "Unknown")
            industry_ps_benchmark = get_industry_ps_benchmark(industry)
            
            # Comparing P/S ratio with the industry benchmark
            ps_comparison = (
                "Above Benchmark" if ps_ratio and industry_ps_benchmark and ps_ratio > industry_ps_benchmark else
                "Below Benchmark" if ps_ratio and industry_ps_benchmark and ps_ratio < industry_ps_benchmark else
                "At Benchmark" if ps_ratio and industry_ps_benchmark and ps_ratio == industry_ps_benchmark else
                "Data Unavailable"
            )
            
            # Return the data
            return {
                "ps_ratio": ps_ratio,
                "industry_ps_benchmark": industry_ps_benchmark,
                "ps_comparison": ps_comparison,
                "recommendation": self._get_ps_recommendation(ps_ratio, industry_ps_benchmark)
            }
        except KeyError:
            return {"error": "Error retrieving data for the stock."}
    
    def _get_ps_recommendation(self, ps_ratio, industry_ps_benchmark):
        if ps_ratio is None or industry_ps_benchmark is None:
            return "Data Unavailable"
        
        if ps_ratio > industry_ps_benchmark:
            return "Sell"
        elif ps_ratio < industry_ps_benchmark:
            return "Buy"
        else:
            return "Hold"

    def _get_industry_pe_benchmark(self):
        """
        Dynamically set the industry P/E benchmark based on the stock's industry.

        Returns:
            float: The industry P/E benchmark, or None if unavailable.
        """
        industry = self.info.get("industry")
        sector = self.info.get("sector")
        
        # Use the helper function to get the benchmark
        return get_industry_pe_benchmark(industry, sector)
    
    def get_pe_ratio(self):
        """
        Calculate the trailing and forward P/E ratios and provide a recommendation.

        Returns:
            dict: A dictionary containing trailing P/E, forward P/E, their comparison,
                  and a recommendation.
        """
        try:
            trailing_pe = self.info.get("trailingPE")
            forward_pe = self.info.get("forwardPE")
            
            result = {
                "trailing_pe": trailing_pe,
                "forward_pe": forward_pe,
                "industry_pe_benchmark": self.industry_pe_benchmark,
                "trailing_pe_comparison": self._compare_to_pe_benchmark(trailing_pe),
                "forward_pe_comparison": self._compare_to_pe_benchmark(forward_pe),
                "recommendation": self._get_pe_recommendation(trailing_pe, forward_pe),
            }
            return result
        except Exception as e:
            return {"error": str(e)}
        
    def _compare_to_pe_benchmark(self, pe_ratio):
        """
        Compare the given P/E ratio to the industry benchmark.

        Args:
            pe_ratio (float): The P/E ratio to compare.

        Returns:
            str: 'Above Benchmark', 'Below Benchmark', or 'Not Available'.
        """
        if pe_ratio is None:
            return "Not Available"
        if pe_ratio > self.industry_pe_benchmark:
            return "Above Benchmark"
        elif pe_ratio < self.industry_pe_benchmark:
            return "Below Benchmark"
        else:
            return "At Benchmark"

    def _get_pe_recommendation(self, trailing_pe, forward_pe):
        """
        Provide a buy/hold/sell recommendation based on P/E ratios.

        Args:
            trailing_pe (float): Trailing P/E ratio.
            forward_pe (float): Forward P/E ratio.

        Returns:
            str: 'Buy', 'Hold', or 'Sell'.
        """
        if trailing_pe is None and forward_pe is None:
            return "Insufficient data for recommendation"

        # Favor forward P/E if both are available
        pe_ratio = forward_pe if forward_pe is not None else trailing_pe

        if pe_ratio < self.industry_pe_benchmark:
            return "Buy"
        elif pe_ratio == self.industry_pe_benchmark:
            return "Hold"
        else:
            return "Sell"
          
    def get_pb_ratio(self):
        try:
            # Fetching the P/B ratio directly from the Yahoo Finance info object
            pb_ratio = self.info.get("priceToBook", None)
            
            if pb_ratio is None:
                return {"error": "P/B ratio data is unavailable for this stock."}
            
            # Get the industry P/B Benchmark
            industry = self.info.get("sector", "Unknown")
            industry_pb_benchmark = get_industry_pb_benchmark(industry)
            
            # Comparing P/B ratio with the industry benchmark
            pb_comparison = "Above Benchmark" if pb_ratio and industry_pb_benchmark and pb_ratio > industry_pb_benchmark else \
                            "Below Benchmark" if pb_ratio and industry_pb_benchmark and pb_ratio < industry_pb_benchmark else \
                            "At Benchmark" if pb_ratio and industry_pb_benchmark and pb_ratio == industry_pb_benchmark else \
                            "Data Unavailable"
            
            # Return the data
            return {
                "pb_ratio": pb_ratio,
                "industry_pb_benchmark": industry_pb_benchmark,
                "pb_comparison": pb_comparison,
                "recommendation": self._get_pb_recommendation(pb_ratio, industry_pb_benchmark)
            }
        except KeyError:
            return {"error": "Error retrieving data for the stock."}
    
    def _get_pb_recommendation(self, pb_ratio, industry_pb_benchmark):
        if pb_ratio is None or industry_pb_benchmark is None:
            return "Data Unavailable"
        
        if pb_ratio > industry_pb_benchmark:
            return "Sell"
        elif pb_ratio < industry_pb_benchmark:
            return "Buy"
        else:
            return "Hold"

    def get_ev_ebitda(self):
        try:
            market_cap = self.info["marketCap"]
            total_debt = self.info["totalDebt"]
            cash = self.info["cash"]
            ebitda = self.info["ebitda"]
            ev = market_cap + total_debt - cash
            ev_ebitda = ev / ebitda
            return ev_ebitda
        except (KeyError, ZeroDivisionError):
            return None

    def get_fcf_yield(self):
        try:
            cashflow = self.stock.cashflow
            fcf = cashflow.loc['Total Cash From Operating Activities'] - cashflow.loc['Capital Expenditures']
            market_cap = self.info["marketCap"]
            fcf_yield = fcf / market_cap
            return fcf_yield
        except (KeyError, ZeroDivisionError):
            return None

    def fetch_all_ratios(self):
        return {
            "P/E Ratio": self.get_pe_ratio(),
            "P/B Ratio": self.get_pb_ratio(),
            "P/S Ratio": self.get_ps_ratio(),
            "PEG Ratio": self.get_peg_ratio(),
            "Dividend Yield": self.get_dividend_yield(),
            "Dividend Payout": self.get_dividend_payout_ratio()
        }

