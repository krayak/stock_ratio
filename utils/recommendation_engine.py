class RecommendationEngine:
    def __init__(self, weights=None, thresholds=None):
        """Initializes the RecommendationEngine with weights and thresholds."""
        self.weights = weights or {
            "Valuation": {
                "P/E Ratio": 0.25,
                "PEG Ratio": 0.1,
                "P/S Ratio": 0.2,
                "P/B Ratio": 0.25,
                "Dividend Yield": 0.1,
                "Dividend Payout": 0.1
            },
            "Profitability": {
                "ROA": 0.3,
                "ROE": 0.4,
                "Net Profit Margin": 0.3
            },
            "Liquidity": {
                "Current Ratio": 0.5,
                "Quick Ratio": 0.5
            },
            "Debt": {
                "Debt-to-Equity Ratio": 0.5,
                "Interest Coverage Ratio": 0.5
            },
            "Efficiency": {
                "Asset Turnover Ratio": 1.0
            }
        }
        self.thresholds = thresholds or {
            "Buy": 70,
            "Hold": 40,
            "Sell": 0
        }

    def calculate_metric_score(self, metric_data):
        """Calculates a score (0-100) for a single metric."""
        if not metric_data or "recommendation" not in metric_data or metric_data["recommendation"] == "Data Unavailable":
            return 0  # Handle cases where metric_data is None or empty

        recommendation = metric_data["recommendation"]
        if recommendation == "Buy":
            return 100
        elif recommendation == "Hold":
            return 50
        elif recommendation == "Sell":
            return 0
        else:
            return 0 # Handle unexpected recommendation strings

    def calculate_category_score(self, category_data, category_name):
        """Calculates the weighted score for a category, handling missing data."""
        if not category_data or category_name not in self.weights:  # Handle missing category data
            return 0

        category_weights = self.weights[category_name]
        category_score = 0
        total_weight_used = 0

        for metric, metric_data in category_data.items():
            if metric in category_weights:
                metric_score = self.calculate_metric_score(metric_data)
                if metric_score != 0:
                    category_score += metric_score * category_weights[metric]
                    total_weight_used += category_weights[metric]

        return category_score / total_weight_used if total_weight_used else 0 #Simplified conditional

    def calculate_overall_score(self, analysis_results):
        """Calculates the overall weighted score, handling missing categories."""
        if not analysis_results: #Handle if analysis_results is empty
            return 0
        overall_score = 0
        total_weight_used = 0
        for category, category_data in analysis_results.items():
            category_score = self.calculate_category_score(category_data, category)
            category_weight = sum(self.weights.get(category, {}).values())
            if category_score != 0:
                overall_score += category_score * category_weight
                total_weight_used += category_weight

        return overall_score / total_weight_used if total_weight_used else 0 #Simplified conditional

    def get_overall_recommendation(self, score):
        """Determines the overall recommendation."""
        if score >= self.thresholds["Buy"]:
            return "Buy"
        elif score >= self.thresholds["Hold"]:
            return "Hold"
        else:
            return "Sell"

    def update_weights(self, new_weights):
        """Updates the weights dictionary."""
        self.weights.update(new_weights)

    def update_thresholds(self, new_thresholds):
        """Updates the thresholds dictionary."""
        self.thresholds.update(new_thresholds)

    def get_category_recommendation(self, category_data, category_name):
        """Gets the category specific recommendation based on the WEIGHTED score."""
        if not category_data or category_name not in self.weights:  # Handle missing category data
            return "Data Unavailable"
        category_score = self.calculate_category_score(category_data, category_name)
        return self.get_overall_recommendation(category_score)
