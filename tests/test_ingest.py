# tests/test_ingest.py
from sqlalchemy import create_engine, text
def test_row_counts():
    e = create_engine("postgresql+psycopg2://bi_user:bi_pass@localhost:5432/retail")
    with e.begin() as c:
        n, = c.execute(text("SELECT COUNT(*) FROM fact_sales")).one()
    assert n > 1_000_000
