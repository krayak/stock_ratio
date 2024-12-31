from stock_ratios.valuation import ValuationRatios
from stock_ratios.profitability import ProfitabilityRatios
from stock_ratios.liquidity import LiquidityRatios
from stock_ratios.debt import DebtRatios
from stock_ratios.efficiency import EfficiencyRatios

class StockRatios:
    def __init__(self, ticker):
        self.ticker = ticker
        self.valuation = ValuationRatios(ticker)
        self.profitability = ProfitabilityRatios(ticker)
        self.liquidity = LiquidityRatios(ticker)
        self.debt = DebtRatios(ticker)
        self.efficiency = EfficiencyRatios(ticker)

    def get_valuation_ratios(self):
        return self.valuation.fetch_all_ratios()

    def get_profitability_ratios(self):
        return self.profitability.fetch_all_ratios()

    def get_liquidity_ratios(self): 
        return self.liquidity.fetch_all_ratios()

    def get_debt_ratios(self): 
        return self.debt.fetch_all_ratios()
    
    def get_efficiency_ratios(self): 
        return self.efficiency.fetch_all_ratios()

    def fetch_all_ratios(self):
        return {
            "Valuation": self.get_valuation_ratios(),
            "Profitability": self.get_profitability_ratios(),
            "Liquidity": self.get_liquidity_ratios(),
            "Debt" : self.get_debt_ratios(),
            "Efficiency": self.get_efficiency_ratios()
        }

