# Retail Sales Performance Analysis

An end-to-end portfolio project for a Business Data Analyst role. It demonstrates data validation, SQL reporting, Python analysis, dashboard-ready KPI exports, and clear business communication.

> **Data note:** `data/orders.csv` is generated locally by the included script. It is fully synthetic, not a client dataset, and does not represent a real business.

## Business question

How do delivered sales and estimated gross profit vary over time, by product category, region, and sales channel? What should a business team investigate next?

## What is included

- `data/orders.csv` — created locally by `src/generate_data.py`: 1,200 synthetic orders with dates, product, category, region, channel, units, discounts, cost, status, and customer type. The generated CSV is not checked into GitHub.
- `sql/analysis.sql` — schema plus reusable SQL queries for KPIs, monthly trends, category/channel comparisons, and data quality.
- `src/generate_data.py` — reproducible synthetic data generator.
- `src/analyze.py` — Python/pandas validation, metric calculations, CSV exports, chart, and findings.
- `reports/business_findings.md` — concise business readout with definitions and caveats.
- `reports/sales_overview.svg` — visual summary.
- `reports/*_performance.csv` — outputs ready to import into Excel or Power BI.

## Run it

Requires Python 3.10+ with pandas.

```bash
python -m pip install pandas
python src/generate_data.py
python src/analyze.py
```

Run `sql/analysis.sql` in PostgreSQL after loading `data/orders.csv` into a table named `orders`. For Excel or Power BI, import the CSV exports from `reports/` and format INR values as currency.

## KPI definitions

- **Delivered net sales:** units × unit price × (1 − discount), delivered orders only.
- **Estimated gross profit:** delivered net sales − units × unit cost. Excludes marketing, shipping, tax, and overhead; it is not accounting profit.
- **Delivered order count:** distinct order IDs with `order_status = 'Delivered'`.
- **Return/cancellation rate:** count of records in that status divided by all records.

## Findings and interpretation

See [`reports/business_findings.md`](reports/business_findings.md). All patterns are descriptive and synthetic. This project demonstrates an analysis workflow; it does not claim employment or client impact.

## Skills demonstrated

SQL (aggregations, CASE, date grouping, quality checks), Python/pandas, KPI design, data validation, visualization, and stakeholder-ready recommendations.

