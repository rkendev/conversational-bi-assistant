#!/usr/bin/env python
import os
import sqlalchemy as sa
import pandas as pd

DSN = os.getenv("POSTGRES_URL", "postgresql+psycopg2://bi_user:bi_pass@localhost:5433/retail")
engine = sa.create_engine(DSN, future=True)

def q(sql: str) -> pd.DataFrame:
    with engine.begin() as conn:
        return pd.read_sql_query(sa.text(sql), conn)

if __name__ == "__main__":
    # sanity
    with engine.connect() as c:
        print("→ sanity:", c.exec_driver_sql("SELECT 1").scalar())

    # list tables
    print("\n→ Tables:")
    with engine.connect() as c:
        rows = c.exec_driver_sql("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema='public'
            ORDER BY 1,2
        """).fetchall()
        for s, t in rows:
            print(f"  {s}.{t}")

    # demo queries
    print("\n→ Monthly revenue (first 5):")
    print(q("SELECT * FROM vw_monthly_revenue ORDER BY month LIMIT 5;").to_string(index=False))

    print("\n→ Top 10 customers:")
    print(q("SELECT * FROM vw_top_customers LIMIT 10;").to_string(index=False))
