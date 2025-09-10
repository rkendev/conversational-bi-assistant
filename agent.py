#!/usr/bin/env python
from dotenv import load_dotenv
load_dotenv()  # load variables from a local .env if present

import os
import sqlalchemy as sa
import pandas as pd

# Use POSTGRES_URL if set; default to 5432 (CI-safe). Locally, set POSTGRES_URL to ...:5433/...
DSN = os.getenv("POSTGRES_URL", "postgresql+psycopg2://bi_user:bi_pass@localhost:5432/retail")
engine = sa.create_engine(DSN, future=True)

def q(sql: str) -> pd.DataFrame:
    """Run a read-only query and return a DataFrame."""
    with engine.begin() as conn:
        return pd.read_sql_query(sa.text(sql), conn)

if __name__ == "__main__":
    # Sanity check
    with engine.connect() as c:
        print("→ sanity:", c.exec_driver_sql("SELECT 1").scalar())

    # List public tables
    print("\n→ Tables:")
    with engine.connect() as c:
        rows = c.exec_driver_sql("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY 1, 2
        """).fetchall()
        for s, t in rows:
            print(f"  {s}.{t}")

    # Demo queries
    print("\n→ Monthly revenue (first 5):")
    print(q("SELECT * FROM vw_monthly_revenue ORDER BY month LIMIT 5;").to_string(index=False))

    print("\n→ Top 10 customers:")
    print(q("SELECT * FROM vw_top_customers LIMIT 10;").to_string(index=False))
