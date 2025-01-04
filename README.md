# Financial Ratios Analyser

---

## **Overview**
This project provides a structured approach to analyzing financial ratios for a company, offering detailed insights into valuation, profitability, liquidity, debt, and efficiency metrics. The analysis is summarized into recommendations for investment decisions based on industry benchmarks and the company’s performance.

This project is a Python module designed to analyze equities using various financial ratios. It focuses on valuation, efficiency, profitability, and debt metrics to provide actionable investment recommendations. The module can be installed via `setup.py` and accessed through a command-line interface (CLI).

The analysis covers the following categories of financial ratios:

- **Valuation Ratios**
- **Profitability Ratios**
- **Liquidity Ratios**
- **Debt Ratios**
- **Efficiency Ratios**

Each category contains multiple metrics that are evaluated against industry benchmarks to provide actionable recommendations.

**Special Note:**  
This framework is designed to assist in the quantitative analysis of various financial ratios and provides a consolidated output to streamline decision-making. However, it is imperative to validate the generated output and avoid blindly following the recommendations. Users should perform initial analysis and cross-check with other relevant data to ensure the soundness of investment decisions.

---

## **Features**

1. **Detailed Ratio Analysis**: Each metric includes:
   - Comparison against industry benchmarks.
   - Recommendations based on the analysis.

2. **Summary**:
   - Overall score for the company.
   - Final investment recommendation (e.g., Buy, Hold, Sell).

3. **Category Recommendations**:
   - High-level recommendations for each category based on the metrics.

4. **Quantitative Ratio Analysis**:
   - **Valuation Ratios**: Price-to-Earnings (P/E), Price-to-Book (P/B), Price-to-Sell (P/S), PEG Ratio, Divident Yield, Dividend Payout
   - **Efficiency Ratios**: Asset Turnover, Inventory Turnover
   - **Profitability Ratios**: Return on Equity (ROE), Return of Asset (ROA), Net Profit Margin, Gross Profit Margin
   - **Debt Ratios**: Debt-to-Equity, Interest Coverage
   - **Liquidity Ratios**: Current Ratio, Quick Ratio
5. **Command-Line Interface (CLI)**: Allows users to input stock ticker symbols and receive ratio calculations and recommendations.
6. **Custom Recommendations**: Compares financial ratios against industry benchmarks to suggest "Buy," "Hold," or "Sell."
7. **Configurable Benchmarks**: Benchmarks for each ratio are stored and managed centrally using a configuration file structure.
8. **Lightweight Dependencies**: Uses `yfinance` for financial data fetching.

## **Configuration**
The config folder stores all benchmark details and global settings in JSON files. Each ratio category has its own configuration file for flexibility and modularity.

---

## **JSON Structure**
The data is organized into a structured JSON format. Below is a breakdown of the main sections:

### **1. Valuation Ratios Output**

```json
{
    "Metric": "P/E Ratio",
    "Forward P/E": "19.5253",
    "Comparison": "Above Benchmark",
    "Trailing P/E": "24.750742"
}
```

### **2. Profitability Ratios Output**

```json
{
    "Metric": "ROA",
    "Comparison": "Within Benchmark",
    "Industry Benchmark (%)": "(4.0, 8.0)",
    "ROA (%)": 4.14,
    "Recommendation": "Hold"
}
```

### **3. Liquidity Ratios Output**

```json
{
    "Metric": "Current Ratio",
    "Comparison": "Within Benchmark",
    "Current Ratio": 1.18,
    "Industry Benchmark": "(0.8, 1.4)",
    "Recommendation": "Hold"
}
```

### **4. Debt Ratios Output**

```json
{
    "Metric": "Debt-to-Equity Ratio",
    "Comparison": "Below Benchmark",
    "Debt-to-Equity Ratio": 0.37,
    "Industry Benchmark": "(0.8, 1.8)",
    "Recommendation": "Buy"
}
```

### **5. Efficiency Ratios Output**

```json
{
    "Metric": "Asset Turnover Ratio",
    "Asset Turnover Ratio": 0.54,
    "Comparison": "Within Benchmark",
    "Industry Benchmark": "(0.4, 0.8)",
    "Recommendation": "Hold"
}
```

### **6. Summary**

```json
{
    "Ticker": "RELIANCE.NS",
    "Overall Score": 77.27272727272727,
    "Overall Recommendation": "Buy"
}
```

### **7. Category Recommendations**

```json
{
    "Valuation": "Buy",
    "Profitability": "Sell",
    "Liquidity": "Sell",
    "Debt": "Sell",
    "Efficiency": "Sell"
}
```

---
## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:krayak/stock_ratio.git
   cd stock_ratio
   pip install -e .
   stock-ratios RELIANCE.NS ## Fetch and perform stock analysis on Reliance
---

## **Dependencies**

- Python 3.10+
- Libraries: None required, but recommended for advanced usage:
  - `yfinance`: For data retrieval.

## **License**

This project is open-source under the MIT License.
---

## **Contact**

For questions or feedback, please reach out to [structbinary<sandeepmahto4@gmail.com>].

