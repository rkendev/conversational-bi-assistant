/* ---------- Monthly revenue per month ---------- */
CREATE OR REPLACE VIEW vw_monthly_revenue AS
SELECT DATE_TRUNC('month', invoice_ts)::date                AS month,
       ROUND(SUM(unit_price * qty)::numeric, 2)             AS revenue
FROM   fact_sales
GROUP  BY 1
ORDER  BY 1;

/* ---------- Lifetime value for top-10 customers ---------- */
CREATE OR REPLACE VIEW vw_top_customers AS
SELECT c."CustomerID"                                       AS customer_id,
       ROUND(SUM(unit_price * qty)::numeric, 2)             AS lifetime_value,
       COUNT(DISTINCT DATE_TRUNC('month', invoice_ts))      AS active_months
FROM   fact_sales f
JOIN   dim_customer c ON c."CustomerID" = f.customer_id
GROUP  BY 1
ORDER  BY lifetime_value DESC
LIMIT  10;
