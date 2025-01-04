import sys
import json
import argparse
from stock_ratios.core import StockRatios
from rich.console import Console
from rich.table import Table

def get_ratios(ticker):
    stock_ratios = StockRatios(ticker)
    ratios = stock_ratios.fetch_all_ratios()
    
    console = Console()

    # Displaying the detailed ratio tables
    for category, data in ratios["analysis_result"].items():
        table = Table(title=f"{category} Ratios")
        
        # Collect all possible headers dynamically across all metrics
        all_headers = set()
        for values in data.values():
            all_headers.update(values.keys())
        
        # Sort headers to ensure consistent order
        all_headers = sorted(all_headers)
        headers = ["Metric"] + list(all_headers)
        
        # Add columns to the table
        table.add_column("Metric", style="cyan", no_wrap=True)
        for header in headers[1:]:
            table.add_column(header, style="green")
        
        # Add rows for each metric
        for metric, values in data.items():
            row = [metric] + [str(values.get(header, "")) for header in headers[1:]]
            table.add_row(*row)
        
        # Print the table for the current category
        console.print(table)
    
    # Displaying the summary table
    summary_table = Table(title="Summary")
    summary_table.add_column("Ticker", style="cyan")
    summary_table.add_column("Overall Score", style="magenta")
    summary_table.add_column("Overall Recommendation", style="green")
    summary_table.add_row(
        ratios["ticker"],
        str(ratios["overall_score"]),
        ratios["overall_recommendation"]
    )
    console.print(summary_table)

    # Displaying the category recommendations
    recommendation_table = Table(title="Category Recommendations")
    recommendation_table.add_column("Category", style="cyan")
    recommendation_table.add_column("Recommendation", style="green")

    for category, recommendation in ratios["category_recommendations"].items():
        recommendation_table.add_row(category, recommendation)

    console.print(recommendation_table)

# def summarize_stock_ratios(ticker):
#     """
#     Summarizes stock ratios by categorizing metrics into Above Benchmark, Below Benchmark, 
#     and Unavailable, and counts overall recommendations (Buy, Sell, Hold), 
#     while assigning a priority number to each ratio.
    
#     Args:
#         ticker (str): Stock ticker symbol.
#         ratios (dict): Dictionary containing stock ratios.
        
#     Returns:
#         dict: Summary of ratios, recommendations, and priorities in JSON format.
#     """

#     try:
#         stock_ratios = StockRatios(ticker)
#         ratios = stock_ratios.fetch_all_ratios()
#         print(f"Stock Ratios for {ticker}:")
#         print(f"{ratios}")
#         summary = {}
#         overall_recommendations = {"Buy": 0, "Sell": 0, "Hold": 0}
#         ratio_priorities = {}

#         # Loop through each category (e.g., "Valuation", "Profitability", etc.)
#         for category, metrics in ratios.items():
#             category_summary = {"Above Benchmark": [], "Below Benchmark": [], "Unavailable": []}

#             # Loop through each metric (e.g., "P/E Ratio", "P/B Ratio", etc.)
#             for metric, details in metrics.items():
#                 # Determine comparison priority (Above Benchmark, Below Benchmark, or Unavailable)
#                 comparison = None
#                 for key in details:
#                     if 'comparison' in key.lower():
#                         comparison = details[key]
#                         break
#                 comparison = comparison or "Unavailable"  # Default to "Unavailable" if no comparison is found

#                 # Determine recommendation priority
#                 recommendation = details.get("Recommendation") or details.get("recommendation", "Hold")
                
#                 # Priority assignment for comparison and recommendation
#                 comparison_priority = {"Above Benchmark": 1, "Below Benchmark": 2, "Unavailable": 3}.get(comparison, 3)
#                 recommendation_priority = {"Buy": 1, "Sell": 2, "Hold": 3}.get(recommendation.split()[0], 3)
                
#                 # Calculate final priority by summing comparison and recommendation priorities
#                 final_priority = comparison_priority + recommendation_priority

#                 # Store the ratio and its priority
#                 ratio_priorities[metric] = final_priority

#                 # Categorize the metric based on its comparison
#                 if comparison == "Above Benchmark":
#                     category_summary["Above Benchmark"].append((metric, final_priority))
#                 elif comparison == "Below Benchmark":
#                     category_summary["Below Benchmark"].append((metric, final_priority))
#                 else:
#                     category_summary["Unavailable"].append((metric, final_priority))

#                 # Tally recommendations
#                 if recommendation.lower().startswith("buy"):
#                     overall_recommendations["Buy"] += 1
#                 elif recommendation.lower().startswith("sell"):
#                     overall_recommendations["Sell"] += 1
#                 else:
#                     overall_recommendations["Hold"] += 1

#             # Store the category summary
#             summary[category] = category_summary

#         # Construct the final result
#         result = {
#             "Stock": ticker,
#             "Summary": summary,
#             "Overall Recommendations": overall_recommendations,
#             "Ratio Priorities": ratio_priorities  # Include ratio priorities
#         }

#         # Print the final result in a nicely formatted JSON
#         print(json.dumps(result, indent=4))
#         # return result  # Return the result for further use or API response

#     except Exception as e:
#         error_result = {
#             "Stock": ticker,
#             "Summary": "Error occurred",
#             "Error": str(e),
#         }
#         print(json.dumps(error_result, indent=4))
#         # return error_result  # Return error details if an exception occurs
def summarize_stock_ratios(ticker):
    """
    Summarizes stock ratios by categorizing metrics into Above Benchmark, Below Benchmark, 
    and Unavailable, and counts overall recommendations (Buy, Sell, Hold), 
    while assigning a priority number to each ratio.
    
    Args:
        ticker (str): Stock ticker symbol.
        
    Returns:
        dict: Summary of ratios, recommendations, and priorities in JSON format.
    """

    try:
        stock_ratios = StockRatios(ticker)
        ratios = stock_ratios.fetch_all_ratios()
        print(f"Stock Ratios for {ticker}:")
        print(json.dumps(ratios, indent=2))
        summary = {}
        overall_recommendations = {"Buy": 0, "Sell": 0, "Hold": 0}
        ratio_priorities = {}

        # Define weights for comparison and recommendation priorities
        comparison_weight = 0.6
        recommendation_weight = 0.4

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
                
                # Assign weights to comparison and recommendation priorities
                comparison_priority = {"Above Benchmark": 1, "Below Benchmark": 2, "Unavailable": 3}.get(comparison, 3)
                recommendation_priority = {"Buy": 1, "Sell": 2, "Hold": 3}.get(recommendation.split()[0], 3)
                
                # Calculate weighted final priority
                final_priority = (comparison_weight * comparison_priority) + (recommendation_weight * recommendation_priority)

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
            "Summary Statement": f"{ticker} has a mix of above and below benchmark ratios, with a total of {sum(overall_recommendations.values())} recommendations.",
            "Summary": summary,
            "Overall Recommendations": overall_recommendations,
            "Ratio Priorities": {
                "Priorities": ratio_priorities,
                "Description": "The priority scores are calculated based on the comparison and recommendation priorities."
            }
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

def main():
    parser = argparse.ArgumentParser(description="Fetch stock ratios")
    parser.add_argument('ticker', type=str, help="Stock ticker symbol")
    
    args = parser.parse_args()
    
    # Get the ratios for the given stock ticker
    get_ratios(args.ticker)
    # summarize_stock_ratios(args.ticker)

if __name__ == "__main__":
    main()
