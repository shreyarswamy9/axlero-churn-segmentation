
"""
Data cleaning for the Online Retail II dataset.
Preserves problematic records using flags wherever possible.
"""

from pathlib import Path
import pandas as pd

from src.dataset import load_raw_data


CLEAN_CSV = Path("data/interim/online_retail_clean.csv")
MAX_REMOVED_PERCENT = 5.0

NON_PRODUCT_CODES = {
    "POST", "DOT", "M", "D", "C2",
    "BANK CHARGES", "AMAZONFEE",
    "ADJUST", "ADJUST2", "TEST001", "TEST002"
}


def clean(df):
    df = df.copy()

    original_rows = len(df)

    # Remove exact duplicate records
    df = df.drop_duplicates().copy()

    removed_percent = (
        (original_rows - len(df)) / original_rows
    ) * 100

    assert removed_percent < MAX_REMOVED_PERCENT, (
        f"Too many rows removed: {removed_percent:.2f}%"
    )

    # Identify important record types
    df["invoice"] = df["invoice"].astype(str)
    df["stock_code"] = df["stock_code"].astype(str)

    df["has_customer_id"] = df["customer_id"].notna()

    df["is_cancellation"] = df["invoice"].str.startswith(
        "C", na=False
    )

    df["is_non_product"] = df["stock_code"].isin(
        NON_PRODUCT_CODES
    )

    df["is_valid_sale"] = (
        (df["quantity"] > 0)
        & (df["price"] > 0)
        & (~df["is_cancellation"])
        & (~df["is_non_product"])
    )

    # Fill missing product descriptions
    df["description"] = df["description"].fillna("Unknown")

    # Cap extreme positive values at the 99.9th percentile
    for column in ["quantity", "price"]:
        positive_values = df.loc[df[column] > 0, column]

        if not positive_values.empty:
            upper_limit = positive_values.quantile(0.999)
            df[column] = df[column].clip(upper=upper_limit)

    # Create useful analysis columns
    df["line_total"] = df["quantity"] * df["price"]

    df["invoice_date"] = pd.to_datetime(
        df["invoice_date"], errors="coerce"
    )

    df["year_month"] = df["invoice_date"].dt.to_period("M").astype(str)

    return df


def main():
    df = load_raw_data()
    cleaned_df = clean(df)

    CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(CLEAN_CSV, index=False)

    print("Data cleaning completed!")
    print("Original and cleaned rows:", len(df), len(cleaned_df))
    print("Rows removed:", len(df) - len(cleaned_df))
    print("Saved file:", CLEAN_CSV)


if __name__ == "__main__":
    main()
