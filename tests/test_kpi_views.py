from dotenv import load_dotenv
load_dotenv()  # read POSTGRES_URL from .env if present

import os
from sqlalchemy import create_engine, text

DSN = os.getenv(
    "POSTGRES_URL",
    "postgresql+psycopg2://bi_user:bi_pass@localhost:5432/retail"  # CI-safe default
)
ENG = create_engine(DSN, future=True)

def test_monthly_revenue_view():
    with ENG.begin() as c:
        months, = c.execute(text("SELECT COUNT(*) FROM vw_monthly_revenue")).one()
    assert months >= 13
