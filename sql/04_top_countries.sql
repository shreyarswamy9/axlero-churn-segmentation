-- 04_top_countries.sql
-- Orders, distinct customers, and total revenue by country (highest revenue first).

SELECT
    country,
    COUNT(DISTINCT invoice)                   AS orders,
    COUNT(DISTINCT customer_id)               AS customers,
    ROUND(SUM(quantity * price)::numeric, 2)  AS revenue
FROM transactions
WHERE LEFT(invoice, 1) <> 'C'
  AND quantity > 0
  AND price > 0
GROUP BY country
ORDER BY revenue DESC;
