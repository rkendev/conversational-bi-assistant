#!/usr/bin/env python
"""
Load Online Retail II → Postgres dimensional model.
Run:
    poetry run python ingest.py --csv data/raw/online_retail_II*.csv
"""
from __future__ import annotations
import argparse, pathlib, pandas as pd
from sqlalchemy import create_engine, text
from dateutil import parser

DSN = "postgresql+psycopg2://bi_user:bi_pass@localhost:5432/retail"
MIGRATION_FILE = pathlib.Path("scripts/01_create_views.sql")


# ---------- helpers ---------------------------------------------------------
def parse_invoice_ts(col: pd.Series) -> pd.Series:
    """Parse every InvoiceDate string into a correct 2009-2011 timestamp."""
    def _one(s: str):
        dt = parser.parse(s, dayfirst=False, fuzzy=True)
        if dt.year < 100:                # 2-digit year → 2000-2069 rule
            dt = dt.replace(year=dt.year + 2000)
        return dt
    return pd.to_datetime(col.apply(_one))


def load_csvs(paths: list[pathlib.Path]) -> pd.DataFrame:
    frames = []
    for p in paths:
        df = pd.read_csv(p, encoding="ISO-8859-1")
        df.rename(
            columns={"Price": "UnitPrice", "Customer ID": "CustomerID", "Invoice": "InvoiceNo"},
            inplace=True,
        )
        frames.append(df)
    out = pd.concat(frames, ignore_index=True)
    out["invoice_ts"] = parse_invoice_ts(out["InvoiceDate"])
    out.drop(columns=["InvoiceDate"], inplace=True)
    return out


# ---------- writers ---------------------------------------------------------


def build_dim_tables(df: pd.DataFrame, eng):
    df[["StockCode", "Description", "UnitPrice"]].drop_duplicates().to_sql(
        "dim_product", eng, if_exists="replace", index=False
    )
    df[["CustomerID", "Country"]].drop_duplicates().to_sql(
        "dim_customer", eng, if_exists="replace", index=False
    )


def build_fact_sales(df: pd.DataFrame, eng):
    fact = df.rename(
        columns={
            "InvoiceNo": "invoice_no",
            "StockCode": "stock_code",
            "CustomerID": "customer_id",
            "Quantity": "qty",
            "UnitPrice": "unit_price",      # <- new tidy name
        }
    )
    fact.to_sql("fact_sales", eng, if_exists="replace", index=False)


def recreate_views(eng):
    with eng.begin() as conn, open(MIGRATION_FILE) as f:
        conn.exec_driver_sql(f.read())
    print("→ KPI views recreated")


# ---------- main ------------------------------------------------------------


def main(csv_paths: list[pathlib.Path]):
    print("reading CSVs …")
    df = load_csvs(csv_paths)
  
    eng = create_engine(DSN)

    # drop views so tables can be replaced
    with eng.begin() as conn:
        conn.execute(text("DROP VIEW IF EXISTS vw_top_customers, vw_monthly_revenue CASCADE;"))

    print("writing dimension tables …")
    build_dim_tables(df, eng)

    print("writing fact table … (≈1 min)")
    build_fact_sales(df, eng)

    with eng.begin() as conn:
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_fact_sales_ts ON fact_sales(invoice_ts);"))

    recreate_views(eng)
    print("Ingest complete")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", nargs="+", required=True, type=pathlib.Path)
    main(ap.parse_args().csv)
