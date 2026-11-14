"""Load the Online Retail II data and move it into PostgreSQL."""

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

RAW_EXCEL = Path("data/raw/online_retail_II.xlsx")
RAW_CSV = Path("data/interim/transactions_raw.csv")

COLUMN_NAMES = {
    "Invoice": "invoice",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "Price": "price",
    "Customer ID": "customer_id",
    "Country": "country",
}


def load_raw_excel() -> pd.DataFrame:
    """Read both sheets of the Excel file and stack them into one table."""
    sheets = pd.read_excel(RAW_EXCEL, sheet_name=None)
    df = pd.concat(sheets.values(), ignore_index=True)
    df = df.rename(columns=COLUMN_NAMES)
    df["invoice"] = df["invoice"].astype(str)
    df["stock_code"] = df["stock_code"].astype(str)
    return df


def load_raw_data() -> pd.DataFrame:
    """Fast loader for teammates: use the CSV copy if it exists."""
    if RAW_CSV.exists():
        return pd.read_csv(
            RAW_CSV,
            parse_dates=["invoice_date"],
            dtype={"invoice": str, "stock_code": str},
        )
    df = load_raw_excel()
    RAW_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(RAW_CSV, index=False)
    return df
