-- 03_monthly_sales.sql
-- Monthly orders and revenue trend for the dashboard overview chart.

SELECT
    DATE_TRUNC('month', invoice_date)::date   AS month,
    COUNT(DISTINCT invoice)                   AS orders,
    ROUND(SUM(quantity * price)::numeric, 2)  AS revenue
FROM transactions
WHERE LEFT(invoice, 1) <> 'C'
  AND quantity > 0
  AND price > 0
GROUP BY 1
ORDER BY 1;
