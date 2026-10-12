# Business findings (synthetic practice data)

## Executive summary
- Delivered orders: **1,097** of 1,200 records.
- Delivered net sales: **INR 1,887,635** after order-level discounts.
- Highest-sales month: **2025-09** (INR 184,264); lowest: **2025-04** (INR 125,619).
- Largest sales category: **Fashion** (INR 559,835).
- Largest sales channel: **Social** (INR 499,640).
- Data QA: 4.5% returned and 4.1% cancelled records; these are excluded from delivered-sales KPIs.

## Recommended next steps
1. Review month-over-month sales dips alongside promotion calendar, stock availability, and traffic. The synthetic dataset does not contain these explanatory fields, so it cannot establish causes.
2. Compare channel **profit** and margin, not just sales, before shifting marketing budget.
3. Track return and cancellation rates by category and region in the live business version.
4. Ask an operations owner to validate order status definitions before using this KPI in a real business review.

## Metric definitions
- **Delivered net sales** = units × unit price × (1 − discount), for delivered orders only.
- **Estimated gross profit** = delivered net sales − units × unit cost. Excludes shipping, marketing, tax, and overhead; it is not accounting profit.
- **Return/cancellation rate** = records in that status ÷ all generated order records.

## Limitations
All records are synthetic and generated for portfolio practice; the patterns do not describe an actual retailer. Product costs, discounts, order mix, and seasonality are simulated. No customer identifiers are included. Findings are descriptive and do not prove causation.

