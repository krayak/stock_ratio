from stock_ratios.valuation import ValuationRatios
from stock_ratios.profitability import ProfitabilityRatios
from stock_ratios.liquidity import LiquidityRatios
from stock_ratios.debt import DebtRatios
from stock_ratios.efficiency import EfficiencyRatios
from utils.recommendation_engine import RecommendationEngine

class StockRatios:
    def __init__(self, ticker):
        self.ticker = ticker
        self.valuation = ValuationRatios(ticker)
        self.profitability = ProfitabilityRatios(ticker)
        self.liquidity = LiquidityRatios(ticker)
        self.debt = DebtRatios(ticker)
        self.efficiency = EfficiencyRatios(ticker)
        self.recommendation_engine = RecommendationEngine()

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
        valuation_results = self.get_valuation_ratios()
        profitability_results = self.get_profitability_ratios()
        liquidity_results = self.get_liquidity_ratios()
        debt_results = self.get_debt_ratios()
        efficiency_results = self.get_efficiency_ratios()

        analysis_results = {
            "Valuation": valuation_results,
            "Profitability": profitability_results,
            "Liquidity": liquidity_results,
            "Debt": debt_results,
            "Efficiency": efficiency_results
        }

        overall_score = self.recommendation_engine.calculate_overall_score(analysis_results)
        overall_recommendation = self.recommendation_engine.get_overall_recommendation(overall_score)
        category_recommendations = {category: self.recommendation_engine.get_category_recommendation(data, category) for category, data in analysis_results.items()}

        return {
            "ticker": self.ticker,
            "analysis_result": analysis_results,
            "overall_score": overall_score,
            "overall_recommendation": overall_recommendation,
            "category_recommendations": category_recommendations
        }


