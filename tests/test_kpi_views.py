from sqlalchemy import create_engine, text

ENG = create_engine("postgresql+psycopg2://bi_user:bi_pass@localhost:5432/retail")

def test_monthly_revenue_view():
    with ENG.begin() as c:
        months, = c.execute(text("SELECT COUNT(*) FROM vw_monthly_revenue")).one()
    assert months >= 13
