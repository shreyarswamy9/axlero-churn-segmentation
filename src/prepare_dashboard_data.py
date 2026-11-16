"""Merge customer segments and churn predictions into one file for Tableau."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

PROCESSED_DIR = Path("data/processed")
SEGMENTS_PATH = PROCESSED_DIR / "customer_segments.csv"
CHURN_PATH = PROCESSED_DIR / "churn_predictions.csv"
OUTPUT_PATH = PROCESSED_DIR / "dashboard_customers.csv"


def generate_sample_inputs() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create temporary sample segment and churn tables from SQL customer-level data."""
    from src.dataset import run_query

    customers = run_query("sql/02_customer_level.sql")
    df = customers[["customer_id", "country", "recency_days", "frequency", "monetary"]].rename(
        columns={"recency_days": "recency"}
    )

    conditions = [
        (df["recency"] <= 45) & (df["frequency"] >= 5) & (df["monetary"] >= 1500),
        (df["recency"] <= 90) & (df["frequency"] >= 2),
        (df["recency"] > 180),
    ]
    choices = ["Champions", "Loyal Customers", "At Risk / Hibernating"]
    df["segment"] = np.select(conditions, choices, default="Potential Loyalists")
    cluster_map = {
        "Champions": 0,
        "Loyal Customers": 1,
        "Potential Loyalists": 2,
        "At Risk / Hibernating": 3,
    }
    df["cluster"] = df["segment"].map(cluster_map)
    segments = df[["customer_id", "country", "recency", "frequency", "monetary", "cluster", "segment"]]

    prob = np.clip((df["recency"] / 365.0) * 0.75 + (1.0 / (df["frequency"] + 1)) * 0.25, 0.02, 0.98)
    churn = pd.DataFrame(
        {
            "customer_id": df["customer_id"],
            "churn_probability": np.round(prob, 4),
            "risk_level": pd.cut(
                prob,
                bins=[0.0, 0.35, 0.65, 1.0],
                labels=["Low", "Medium", "High"],
            ),
        }
    )
    return segments, churn


def build_dashboard_dataset(use_sample: bool = False) -> pd.DataFrame:
    """Merge segments and churn predictions into dashboard_customers.csv."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    if use_sample or not (SEGMENTS_PATH.exists() and CHURN_PATH.exists()):
        print("Using sample segment/churn inputs generated from sql/02_customer_level.sql...")
        segments, churn = generate_sample_inputs()
    else:
        segments = pd.read_csv(SEGMENTS_PATH)
        churn = pd.read_csv(CHURN_PATH)

    dashboard = segments.merge(churn, on="customer_id", how="left")
    dashboard.to_csv(OUTPUT_PATH, index=False)
    print(dashboard.head())
    print(f"{len(dashboard):,} customers written to {OUTPUT_PATH}")
    return dashboard


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare customer dataset for Tableau.")
    parser.add_argument("--sample", action="store_true", help="Generate sample inputs if team CSVs are not ready.")
    args = parser.parse_args()
    build_dashboard_dataset(use_sample=args.sample)
