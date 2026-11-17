# Dashboard Overview & Business Insights

## Architecture
Customer transaction data is extracted from PostgreSQL via parameterized SQL scripts (`sql/01_data_quality_checks.sql` through `sql/04_top_countries.sql`), combined with K-Means RFM segments and 90-day churn predictions via `src/prepare_dashboard_data.py`, and visualized in a 3-page interactive Tableau Public workbook.

## Pages & Actionability
1. **Executive Overview**: Tracks total revenue, active customer count, total orders, 25-month revenue seasonality, and top 10 revenue-generating countries.
2. **Customer Segments**: Compares customer volume, revenue share, and average RFM metrics across segments alongside targeted retention playbooks.
3. **Churn Risk & Action List**: Enables marketing managers to filter high-risk customers by segment and country, prioritized by predicted churn probability.
