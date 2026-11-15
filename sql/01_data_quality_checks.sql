-- 01_data_quality_checks.sql
-- Audit raw Online Retail II transactions before cleaning and feature engineering.

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT invoice) AS total_invoices,
    COUNT(DISTINCT customer_id) AS distinct_customers,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS missing_customer_id_rows,
    ROUND(
        100.0 * SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS missing_customer_id_pct,
    SUM(CASE WHEN LEFT(invoice, 1) = 'C' THEN 1 ELSE 0 END) AS cancelled_invoice_rows,
    SUM(CASE WHEN quantity <= 0 THEN 1 ELSE 0 END) AS non_positive_qty_rows,
    SUM(CASE WHEN price <= 0 THEN 1 ELSE 0 END) AS non_positive_price_rows,
    MIN(invoice_date) AS min_invoice_date,
    MAX(invoice_date) AS max_invoice_date
FROM transactions;
