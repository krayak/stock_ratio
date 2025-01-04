
# Financial Ratios Analyser

---

## **Overview**

This Python module analyzes financial ratios for companies, offering insights into valuation, profitability, liquidity, debt, and efficiency. It provides actionable investment recommendations based on these metrics, compared against industry benchmarks.

The analysis includes:

- **Valuation Ratios**
- **Profitability Ratios**
- **Liquidity Ratios**
- **Debt Ratios**
- **Efficiency Ratios**

This tool aims to assist in quantitative financial analysis but should not be solely relied upon for investment decisions. Cross-check with other data sources for comprehensive analysis.

---

## **Features**

- **Detailed Ratio Analysis**: Metrics compared to industry benchmarks with recommendations.
- **Summary**: Overall company score and investment recommendation (e.g., Buy, Hold, Sell).
- **Category Recommendations**: High-level recommendations for each ratio category.
- **Quantitative Analysis**:
  - **Valuation**: P/E, P/B, P/S, PEG Ratio, Dividend Yield & Payout
  - **Efficiency**: Asset & Inventory Turnover
  - **Profitability**: ROE, ROA, Net & Gross Profit Margin
  - **Debt**: Debt-to-Equity, Interest Coverage
  - **Liquidity**: Current & Quick Ratios
- **CLI**: Input stock tickers and receive ratio analysis and recommendations.
- **Custom Recommendations**: "Buy," "Hold," or "Sell" suggestions based on financial ratios and benchmarks.
- **Configurable Benchmarks**: Central management of benchmarks via configuration files.
- **Lightweight**: Uses `yfinance` for data fetching.

---

## **Weights of Each Ratio**

The following are the weights assigned to each financial ratio for the final recommendation calculation:

- **Valuation Ratios**:
  - **P/E Ratio**: 0.25
  - **PEG Ratio**: 0.1
  - **P/S Ratio**: 0.2
  - **P/B Ratio**: 0.25
  - **Dividend Yield**: 0.1
  - **Dividend Payout**: 0.1

- **Profitability Ratios**:
  - **ROA**: 0.3
  - **ROE**: 0.4
  - **Net Profit Margin**: 0.3

- **Liquidity Ratios**:
  - **Current Ratio**: 0.5
  - **Quick Ratio**: 0.5

- **Debt Ratios**:
  - **Debt-to-Equity Ratio**: 0.5
  - **Interest Coverage Ratio**: 0.5

- **Efficiency Ratios**:
  - **Asset Turnover Ratio**: 1.0

These weights determine how much each ratio contributes to the final investment recommendation. The recommendation engine calculates a weighted score for each category and provides a consolidated recommendation for the company.

---

## **Stock Ticker Format**

- **For Indian Stocks**:  
  - When analyzing Indian stocks, please append `.NS` (for National Stock Exchange) or `.BS` (for Bombay Stock Exchange) to the ticker symbol.  
  - **Example**: `RELIANCE.NS`, `TATAMOTORS.BS`
  
- **For USA Stocks**:  
  - For US-based stocks, only the ticker symbol is needed (e.g., `AAPL`, `GOOGL`).  
  - It is recommended to verify the ticker symbol via Yahoo Finance for accuracy.

Note: The industry benchmark is set as per Indian market standards. If you are performing analysis for stocks outside India, you may need to adjust the benchmarks accordingly for the specific country.

---

## **Configuration**

Benchmark data and global settings are stored in the `config` folder as JSON files, with separate files for each ratio category.

---

## **JSON Structure**

### **Example Outputs**

- **Valuation Ratio (P/E)**:
  ```json
  {
      "Metric": "P/E Ratio",
      "Forward P/E": "19.5253",
      "Comparison": "Above Benchmark",
      "Trailing P/E": "24.750742"
  }
  ```

- **Profitability Ratio (ROA)**:
  ```json
  {
      "Metric": "ROA",
      "Comparison": "Within Benchmark",
      "Industry Benchmark (%)": "(4.0, 8.0)",
      "ROA (%)": 4.14,
      "Recommendation": "Hold"
  }
  ```

- **Summary**:
  ```json
  {
      "Ticker": "RELIANCE.NS",
      "Overall Score": 77.27,
      "Overall Recommendation": "Buy"
  }
  ```

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone git@github.com:krayak/stock_ratio.git
   cd stock_ratio
   pip install -e .
   stock-ratios RELIANCE.NS
   ```

---

## **Dependencies**

- Python 3.10+
- `yfinance` for financial data retrieval.

---

## **License**

MIT License.

---

## **Contact**

For feedback or questions, contact [sandeepmahto4@gmail.com].
