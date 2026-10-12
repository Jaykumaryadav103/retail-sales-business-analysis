-- Retail Sales Performance Analysis | PostgreSQL
-- Load data/orders.csv into public.orders before running these queries.

CREATE TABLE IF NOT EXISTS orders (
  order_id TEXT PRIMARY KEY,
  order_date DATE NOT NULL,
  region TEXT NOT NULL,
  category TEXT NOT NULL,
  product TEXT NOT NULL,
  sales_channel TEXT NOT NULL,
  units INTEGER NOT NULL CHECK (units > 0),
  unit_price_inr NUMERIC(12,2) NOT NULL CHECK (unit_price_inr >= 0),
  discount_pct NUMERIC(5,2) NOT NULL CHECK (discount_pct BETWEEN 0 AND 1),
  unit_cost_inr NUMERIC(12,2) NOT NULL CHECK (unit_cost_inr >= 0),
  order_status TEXT NOT NULL CHECK (order_status IN ('Delivered','Cancelled','Returned')),
  customer_type TEXT NOT NULL CHECK (customer_type IN ('New','Returning'))
);

-- 1. KPI snapshot: exclude non-delivered orders from sales and profit.
SELECT COUNT(DISTINCT order_id) AS delivered_orders,
       ROUND(SUM(units * unit_price_inr * (1 - discount_pct)), 2) AS net_sales_inr,
       ROUND(SUM(units * (unit_price_inr * (1 - discount_pct) - unit_cost_inr)), 2) AS estimated_gross_profit_inr,
       ROUND(100.0 * SUM(units * (unit_price_inr * (1 - discount_pct) - unit_cost_inr)) /
         NULLIF(SUM(units * unit_price_inr * (1 - discount_pct)), 0), 2) AS gross_margin_pct
FROM orders WHERE order_status = 'Delivered';

-- 2. Monthly trend.
SELECT DATE_TRUNC('month', order_date)::date AS month,
       COUNT(DISTINCT order_id) AS delivered_orders,
       ROUND(SUM(units * unit_price_inr * (1 - discount_pct)), 2) AS net_sales_inr,
       ROUND(SUM(units * (unit_price_inr * (1 - discount_pct) - unit_cost_inr)), 2) AS estimated_gross_profit_inr
FROM orders WHERE order_status = 'Delivered'
GROUP BY 1 ORDER BY 1;

-- 3. Category performance; sales and margin together avoid ranking on revenue alone.
SELECT category,
       COUNT(DISTINCT order_id) AS delivered_orders,
       ROUND(SUM(units * unit_price_inr * (1 - discount_pct)), 2) AS net_sales_inr,
       ROUND(SUM(units * (unit_price_inr * (1 - discount_pct) - unit_cost_inr)), 2) AS estimated_gross_profit_inr,
       ROUND(100.0 * SUM(units * (unit_price_inr * (1 - discount_pct) - unit_cost_inr)) /
         NULLIF(SUM(units * unit_price_inr * (1 - discount_pct)), 0), 2) AS gross_margin_pct
FROM orders WHERE order_status = 'Delivered'
GROUP BY category ORDER BY net_sales_inr DESC;

-- 4. Channel and region cuts.
SELECT sales_channel, region, COUNT(DISTINCT order_id) AS delivered_orders,
       ROUND(SUM(units * unit_price_inr * (1 - discount_pct)), 2) AS net_sales_inr,
       ROUND(SUM(units * (unit_price_inr * (1 - discount_pct) - unit_cost_inr)), 2) AS estimated_gross_profit_inr
FROM orders WHERE order_status = 'Delivered'
GROUP BY sales_channel, region ORDER BY net_sales_inr DESC;

-- 5. Basic data quality checks.
SELECT order_status, COUNT(*) AS records,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_all_records
FROM orders GROUP BY order_status ORDER BY records DESC;

SELECT COUNT(*) AS rows,
       COUNT(DISTINCT order_id) AS distinct_order_ids,
       COUNT(*) FILTER (WHERE order_date IS NULL OR region IS NULL OR category IS NULL) AS missing_required_fields,
       COUNT(*) FILTER (WHERE units <= 0 OR discount_pct NOT BETWEEN 0 AND 1) AS invalid_numeric_rows
FROM orders;

