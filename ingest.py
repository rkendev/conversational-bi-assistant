#!/usr/bin/env python
"""
Load Online Retail II CSV → Postgres dimensional model.
Usage:
    poetry run python ingest.py --csv data/raw/online_retail_II.csv
"""
import argparse, pathlib, pandas as pd
from sqlalchemy import create_engine, text

DSN = "postgresql+psycopg2://bi_user:bi_pass@localhost:5432/retail"

def build_dim_tables(df: pd.DataFrame, engine):
    # products
    prod_cols = ["StockCode", "Description", "UnitPrice"]
    df[prod_cols].drop_duplicates().to_sql(
        "dim_product", engine, if_exists="replace", index=False
    )
    # customers
    cust_cols = ["CustomerID", "Country"]
    df[cust_cols].drop_duplicates().to_sql(
        "dim_customer", engine, if_exists="replace", index=False
    )

def build_fact_sales(df: pd.DataFrame, engine):
    fact = df.copy()
    fact.rename(
        columns={
            "InvoiceNo": "invoice_no",
            "StockCode": "stock_code",
            "CustomerID": "customer_id",
            "Quantity": "qty",
            "InvoiceDate": "invoice_ts",
        },
        inplace=True,
    )
    fact.to_sql("fact_sales", engine, if_exists="replace", index=False)

def main(csv_paths: list[pathlib.Path]):
    print("? reading CSVs …")
    df = load_csvs(csv_paths)

    print("here 1")
    engine = create_engine(DSN)
    print("here 2")    
    build_dim_tables(df, engine)
    print("here 3")    
    build_fact_sales(df, engine)
    print("here 4")

    with engine.begin() as conn:
        conn.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_fact_sales_ts "
                "ON fact_sales(invoice_ts);"
            )
        )

    print("Ingest complete ?")


def load_csvs(paths):
    dfs = []
    for p in paths:
        d = pd.read_csv(p, encoding="ISO-8859-1")
        d.rename(columns={
            "Price": "UnitPrice",
            "Customer ID": "CustomerID",
            "Invoice": "InvoiceNo",
        }, inplace=True)
        dfs.append(d)
    return pd.concat(dfs, ignore_index=True)    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", nargs="+", required=True, type=pathlib.Path,
                        help="One or more Online Retail II CSVs")
    main(parser.parse_args().csv)
