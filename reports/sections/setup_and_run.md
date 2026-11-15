# Setup and how to run (draft for the README)

_Draft written 15 Nov; will be moved into README.md once all scripts are merged._

## Setup

1. Install Python 3.10+ and Git.
2. Clone the repo and create a virtual environment:

```
git clone https://github.com/shreyarswamy9/axlero-churn-segmentation.git
cd axlero-churn-segmentation
python -m venv venv
venv\Scripts\activate        (Windows)
source venv/bin/activate     (Mac/Linux)
pip install -r requirements.txt
```

3. Download the UCI Online Retail II dataset and place `online_retail_II.xlsx` in `data/raw/`.
4. Optional, for the SQL step: install PostgreSQL, create a database called `axlero`, and add a `.env` file with `DATABASE_URL=postgresql://postgres:<password>@localhost:5432/axlero`. The `.env` file is ignored by Git.

## How to run (in order)

```
python -m src.dataset                # optional: loads raw data into PostgreSQL
python -m src.cleaning               # writes data/interim/online_retail_clean.csv
python -m src.features               # writes data/processed/customer_segments.csv
python -m src.modeling.train         # trains models, saves models/ and reports/churn_metrics.json
python -m src.modeling.predict       # writes data/processed/churn_predictions.csv
python -m src.prepare_dashboard_data # writes data/processed/dashboard_customers.csv
```

## Data audit baseline (from sql/01_data_quality_checks.sql)

| Measure | Value |
| --- | --- |
| Raw transaction rows | 1,067,371 |
| Rows missing a customer ID | 22.77% |
| Cancelled invoice rows | 19,494 |
| Clean customers (customer-level query) | 5,878 |
