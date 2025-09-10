import os, sqlalchemy as sa, pandas as pd
DSN = os.getenv("POSTGRES_URL", "postgresql+psycopg2://bi_user:bi_pass@localhost:5433/retail")
eng = sa.create_engine(DSN, future=True)

def test_fact_sales_exists():
    with eng.begin() as c:
        n = c.exec_driver_sql("SELECT COUNT(*) FROM fact_sales").scalar()
    assert n > 0

def test_monthly_revenue_view():
    with eng.begin() as c:
        df = pd.read_sql_query("SELECT * FROM vw_monthly_revenue ORDER BY month LIMIT 3", c)
    assert {"month","revenue"}.issubset(df.columns)
    assert len(df) >= 1
