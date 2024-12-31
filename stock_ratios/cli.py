import sys
import json
import argparse
from stock_ratios.core import StockRatios

def get_ratios(ticker):
    stock_ratios = StockRatios(ticker)
    ratios = stock_ratios.fetch_all_ratios()
    
    # Output the ratios to the console
    print(f"Stock Ratios for {ticker}:")
    print(f"{ratios}")
    for category, ratio_dict in ratios.items():
        print(f"\n{category}:")
        for ratio_name, value in ratio_dict.items():
            print(f"  {ratio_name}: {value if value is not None else 'N/A'}")

def summarize_stock_ratios(ticker):
    """
    Summarizes stock ratios by categorizing metrics into Above Benchmark, Below Benchmark, 
    and Unavailable, and counts overall recommendations (Buy, Sell, Hold), 
    while assigning a priority number to each ratio.
    
    Args:
        ticker (str): Stock ticker symbol.
        ratios (dict): Dictionary containing stock ratios.
        
    Returns:
        dict: Summary of ratios, recommendations, and priorities in JSON format.
    """

    try:
        stock_ratios = StockRatios(ticker)
        ratios = stock_ratios.fetch_all_ratios()
        summary = {}
        overall_recommendations = {"Buy": 0, "Sell": 0, "Hold": 0}
        ratio_priorities = {}

        # Loop through each category (e.g., "Valuation", "Profitability", etc.)
        for category, metrics in ratios.items():
            category_summary = {"Above Benchmark": [], "Below Benchmark": [], "Unavailable": []}

            # Loop through each metric (e.g., "P/E Ratio", "P/B Ratio", etc.)
            for metric, details in metrics.items():
                # Determine comparison priority (Above Benchmark, Below Benchmark, or Unavailable)
                comparison = None
                for key in details:
                    if 'comparison' in key.lower():
                        comparison = details[key]
                        break
                comparison = comparison or "Unavailable"  # Default to "Unavailable" if no comparison is found

                # Determine recommendation priority
                recommendation = details.get("Recommendation") or details.get("recommendation", "Hold")
                
                # Priority assignment for comparison and recommendation
                comparison_priority = {"Above Benchmark": 1, "Below Benchmark": 2, "Unavailable": 3}.get(comparison, 3)
                recommendation_priority = {"Buy": 1, "Sell": 2, "Hold": 3}.get(recommendation.split()[0], 3)
                
                # Calculate final priority by summing comparison and recommendation priorities
                final_priority = comparison_priority + recommendation_priority

                # Store the ratio and its priority
                ratio_priorities[metric] = final_priority

                # Categorize the metric based on its comparison
                if comparison == "Above Benchmark":
                    category_summary["Above Benchmark"].append((metric, final_priority))
                elif comparison == "Below Benchmark":
                    category_summary["Below Benchmark"].append((metric, final_priority))
                else:
                    category_summary["Unavailable"].append((metric, final_priority))

                # Tally recommendations
                if recommendation.lower().startswith("buy"):
                    overall_recommendations["Buy"] += 1
                elif recommendation.lower().startswith("sell"):
                    overall_recommendations["Sell"] += 1
                else:
                    overall_recommendations["Hold"] += 1

            # Store the category summary
            summary[category] = category_summary

        # Construct the final result
        result = {
            "Stock": ticker,
            "Summary": summary,
            "Overall Recommendations": overall_recommendations,
            "Ratio Priorities": ratio_priorities  # Include ratio priorities
        }

        # Print the final result in a nicely formatted JSON
        print(json.dumps(result, indent=4))
        # return result  # Return the result for further use or API response

    except Exception as e:
        error_result = {
            "Stock": ticker,
            "Summary": "Error occurred",
            "Error": str(e),
        }
        print(json.dumps(error_result, indent=4))
        # return error_result  # Return error details if an exception occurs

def main():
    parser = argparse.ArgumentParser(description="Fetch stock ratios")
    parser.add_argument('ticker', type=str, help="Stock ticker symbol")
    
    args = parser.parse_args()
    
    # Get the ratios for the given stock ticker
    # get_ratios(args.ticker)
    summarize_stock_ratios(args.ticker)

if __name__ == "__main__":
    main()
