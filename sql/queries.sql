-- =========================================================
-- E-Commerce Sales Analysis - SQL Queries
-- =========================================================


-- View all records from the cleaned orders table
SELECT *
FROM ecommerce_sales_db.orders_cleaned;


-- Select the project database
USE ecommerce_sales_db;


-- =========================================================
-- 1. KPI Summary
-- =========================================================

CREATE OR REPLACE VIEW vw_kpi_summary AS

SELECT
    SUM(Amount) AS TotalRevenue,
    SUM(Profit) AS TotalProfit,
    SUM(Quantity) AS TotalQuantity

FROM orders_cleaned;


-- =========================================================
-- 2. Monthly Sales Analysis
-- =========================================================

CREATE OR REPLACE VIEW vw_monthly_sales AS

SELECT
    Year,
    Month,
    Month_Name,
    SUM(Amount) AS MonthlyRevenue

FROM orders_cleaned

GROUP BY
    Year,
    Month,
    Month_Name

ORDER BY
    Year,
    Month;


-- =========================================================
-- 3. State-wise Sales Analysis
-- =========================================================

CREATE OR REPLACE VIEW vw_state_sales AS

SELECT
    State,
    SUM(Amount) AS TotalRevenue,
    SUM(Profit) AS TotalProfit

FROM orders_cleaned

GROUP BY State

ORDER BY TotalRevenue DESC;


-- =========================================================
-- 4. Category-wise Sales Analysis
-- =========================================================

CREATE OR REPLACE VIEW vw_category_sales AS

SELECT
    Category,
    SUM(Amount) AS TotalRevenue,
    SUM(Profit) AS TotalProfit

FROM orders_cleaned

GROUP BY Category

ORDER BY TotalRevenue DESC;


-- =========================================================
-- 5. Top 10 Customers
-- =========================================================

CREATE OR REPLACE VIEW vw_top_customers AS

SELECT
    CustomerName,
    SUM(Amount) AS Revenue

FROM orders_cleaned

GROUP BY CustomerName

ORDER BY Revenue DESC

LIMIT 10;


-- =========================================================
-- 6. Subcategory Profitability
-- =========================================================

CREATE OR REPLACE VIEW vw_subcategory_profitability AS

SELECT
    Category,
    SubCategory,
    SUM(Amount) AS TotalRevenue,
    SUM(Profit) AS TotalProfit

FROM orders_cleaned

GROUP BY
    Category,
    SubCategory

ORDER BY TotalProfit DESC;


-- =========================================================
-- 7. NEW: Loss-Making Orders Analysis
-- =========================================================

CREATE OR REPLACE VIEW vw_loss_making_orders AS

SELECT
    Category,
    COUNT(*) AS Loss_Order_Count,
    SUM(Amount) AS Sales_From_Loss_Orders,
    SUM(Profit) AS Total_Loss

FROM orders_cleaned

WHERE Profit < 0

GROUP BY Category

ORDER BY Total_Loss ASC;

-- =========================================================
-- 8. Category Performance with Profit Margin
-- =========================================================

CREATE OR REPLACE VIEW vw_category_performance AS
SELECT
    Category,
    SUM(Amount) AS TotalRevenue,
    SUM(Profit) AS TotalProfit,
    ROUND(SUM(Profit) / SUM(Amount) * 100, 2) AS ProfitMarginPct
FROM orders_cleaned
GROUP BY Category
ORDER BY TotalRevenue DESC;

-- =========================================================
-- 9. Top Customers with Profitability
-- =========================================================

CREATE OR REPLACE VIEW vw_customer_performance AS
SELECT
    CustomerName,
    SUM(Amount) AS TotalRevenue,
    SUM(Profit) AS TotalProfit,
    COUNT(DISTINCT Order_ID) AS OrderCount,
    ROUND(SUM(Profit) / SUM(Amount) * 100, 2) AS ProfitMarginPct
FROM orders_cleaned
GROUP BY CustomerName
ORDER BY TotalRevenue DESC
LIMIT 10;

-- =========================================================
-- 10. Loss-Making Orders by Category
-- =========================================================

CREATE OR REPLACE VIEW vw_loss_making_orders AS
SELECT
    Category,
    COUNT(*) AS Loss_Order_Count,
    SUM(Amount) AS Sales_From_Loss_Orders,
    SUM(Profit) AS Total_Loss
FROM orders_cleaned
WHERE Profit < 0
GROUP BY Category
ORDER BY Total_Loss ASC;