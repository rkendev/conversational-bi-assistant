import os
from sqlalchemy import create_engine, text

DSN = os.getenv(
    "POSTGRES_URL",
    "postgresql+psycopg2://bi_user:bi_pass@localhost:5432/retail"
)
ENG = create_engine(DSN)

def test_monthly_revenue_view():
    with ENG.begin() as c:
        months, = c.execute(text("SELECT COUNT(*) FROM vw_monthly_revenue")).one()
    assert months >= 13
