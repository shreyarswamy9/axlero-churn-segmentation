-- 02_customer_level.sql
-- Aggregate valid transactions into customer-level RFM and behavioral features.

WITH clean_transactions AS (
    SELECT
        CAST(customer_id AS BIGINT) AS customer_id,
        invoice,
        stock_code,
        quantity,
        invoice_date,
        price,
        quantity * price AS line_total,
        country
    FROM transactions
    WHERE customer_id IS NOT NULL
      AND LEFT(invoice, 1) <> 'C'
      AND quantity > 0
      AND price > 0
),
snapshot AS (
    SELECT MAX(invoice_date) AS max_date
    FROM clean_transactions
)
SELECT
    c.customer_id,
    MAX(c.country) AS country,
    MIN(c.invoice_date) AS first_purchase_date,
    MAX(c.invoice_date) AS last_purchase_date,
    EXTRACT(DAY FROM (s.max_date - MAX(c.invoice_date)))::INT AS recency_days,
    COUNT(DISTINCT c.invoice) AS frequency,
    ROUND(SUM(c.line_total)::NUMERIC, 2) AS monetary,
    SUM(c.quantity) AS total_items,
    COUNT(DISTINCT c.stock_code) AS unique_products,
    ROUND((SUM(c.line_total) / NULLIF(COUNT(DISTINCT c.invoice), 0))::NUMERIC, 2) AS avg_order_value
FROM clean_transactions c
CROSS JOIN snapshot s
GROUP BY c.customer_id, s.max_date
ORDER BY monetary DESC;
