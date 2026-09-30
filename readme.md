# Indian E-Commerce Sales Analysis

An end-to-end **Data Analytics project** analyzing Indian e-commerce sales data using **Python, SQL, and Power BI**.

The project covers data cleaning, feature engineering, exploratory analysis, profitability analysis, customer performance, loss-making analysis, SQL-based business analysis, automated visualizations, and an interactive Power BI dashboard.

---

## Project Overview

The objective of this project is to transform raw Indian e-commerce sales data into meaningful business insights.

The analysis focuses on:

- Sales and profit performance
- Monthly sales and profit trends
- Category and sub-category profitability
- State-wise sales and profitability
- Customer performance
- Loss-making records and categories
- Sales target comparison
- Interactive business dashboards

### Project Workflow

**Raw Data → Python Data Processing → SQL Analytics → Power BI Dashboard → Business Insights**

---

## Tools & Technologies

| Tool / Technology | Purpose |
|---|---|
| **Python 3.13.5** | Data cleaning, transformation and analysis |
| **Pandas** | Data manipulation and aggregation |
| **NumPy** | Numerical operations |
| **Matplotlib** | Data visualization |
| **Seaborn** | Statistical visualization |
| **MySQL** | SQL analysis and business queries |
| **Power BI** | Interactive dashboard and KPI analysis |
| **Jupyter Notebook** | Exploratory analysis |
| **VS Code** | Development environment |
| **ReportLab** | Automated PDF reporting |

---

## Dataset

### Raw Files

- `List of Orders.csv`
- `Order Details.csv`
- `Sales Target.csv`

### Processed Data

The raw datasets were cleaned, transformed and combined into:

`data/merged_orders_cleaned.csv`

A SQL-ready version was also prepared:

`data/orders_sql_ready.csv`

---

## Data Processing

Python was used to prepare the data for analysis.

The workflow includes:

1. Loading raw CSV files
2. Cleaning and preparing the data
3. Standardizing date fields
4. Merging order-related datasets
5. Creating time-based features
6. Preparing the cleaned master dataset
7. Generating analysis-ready CSV outputs

### Time Features

The analysis includes:

- Year
- Month
- Month Name
- Quarter
- Day
- Weekday
- Weekday Name

---

## Business Analysis

The project analyzes:

### Sales Analysis

- Total sales
- Monthly sales trends
- Category-wise sales
- State-wise sales

### Profitability Analysis

- Total profit
- Monthly profit trends
- Category profitability
- Sub-category profitability
- State profitability
- Profit margin
- Loss-making records

### Customer Analysis

- Top customers by revenue
- Customer order count
- Customer profit
- Customer profit margin

### Target Analysis

- Monthly sales compared with sales targets

---

## SQL Analytics

MySQL is used for business-focused SQL analysis.

The project includes:

- Overall sales and profit analysis
- Monthly sales analysis
- State-wise sales and profit
- Category performance
- Customer performance
- Profit margin analysis
- Loss-making analysis
- Top customer analysis
- Sub-category profitability
- SQL views

SQL files are available in:

`sql/`

---

## Python Analysis Outputs

The generated analysis results are available in the `outputs/` folder.

Important outputs include:

- `category_profitability.csv`
- `category_sales.csv`
- `customer_performance.csv`
- `loss_making_orders_by_category.csv`
- `monthly_profit_trend.csv`
- `monthly_sales.csv`
- `monthly_sales_vs_target.csv`
- `state_profitability.csv`
- `state_sales.csv`
- `top_customers.csv`
- `subcategory_profit_top10.csv`
- `subcategory_profit_bottom10.csv`

---

## Power BI Dashboard

The project includes an interactive Power BI dashboard.

### Dashboard Features

- Total Sales
- Total Profit
- Total Quantity Sold
- Sales vs Profit
- Monthly Sales Trend
- Category-wise Sales
- State-wise Sales
- Year filter
- Category filter

Power BI dashboard:

`PowerBi/Ecommerce_Sales_Analytics_Dashboard.pbix`

---

## Python Visualizations

Python visualizations are stored in:

`outputs/plots/`

The project includes:

- Category-wise sales
- Category-wise profit
- Monthly sales trend
- Monthly profit trend
- State-wise sales
- State-wise profit
- Top customers

---

## Key Insights

Based on the analysis:

- Electronics generates the highest category-level sales.
- Clothing generates the highest total profit among the three major categories.
- Furniture has a lower profit contribution compared with its sales contribution.
- Monthly sales fluctuate across the analyzed period.
- Profitability varies significantly across states.
- High-revenue customers do not always generate high profit.
- Loss-making records are present across all major categories.
- Sales performance and profitability do not always move together.

---

## Project Structure

```text
indian-ecommerce-sales-analysis/
│
├── data/
│   ├── List of Orders.csv
│   ├── Order Details.csv
│   ├── Sales Target.csv
│   ├── merged_orders.csv
│   ├── merged_orders_cleaned.csv
│   └── orders_sql_ready.csv
│
├── notebooks/
│   └── ecommerce_analysis.ipynb
│
├── scripts/
│   ├── analysis.py
│   ├── report_generator.py
│   └── visualizations.py
│
├── sql/
│   ├── initial.sql
│   ├── advanced_analytics.sql
│   ├── final.sql
│   ├── queries.sql
│   └── stored_procedures.sql
│
├── outputs/
│   ├── CSV analysis results
│   ├── PDF reports
│   └── plots/
│
├── PowerBi/
│   ├── Ecommerce_Sales_Analytics_Dashboard.pbix
│   └── Ecommerce_Dashboard_PowerBi.pdf
│
├── .gitignore
├── readme.md
└── requirements.txt

## Author

**Shruti Nagave**

Aspiring Data Analyst | Python | SQL | Power BI

- GitHub: [shrutinagave30](https://github.com/shrutinagave30)
