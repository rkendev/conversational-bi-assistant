# Conversational BI Assistant
*(LLM + Model Context Protocol + PostgreSQL)*

Ask business questions in plain English – the agent converts them to SQL through **MCP**, runs them on Postgres, and replies with concise insights.

---

## 1. What this project is

| Layer            | Tech                         | Purpose                                                                 |
|------------------|------------------------------|-------------------------------------------------------------------------|
| Data warehouse   | **PostgreSQL 15**            | Stores the Online Retail II dimensional model (`dim_product`, `dim_customer`, `fact_sales`) |
| Access layer     | **Model Context Protocol**   | Exposes the database schema & query endpoint to any LLM agent           |
| Agent            | **LangChain + Python**       | Translates user prompts → MCP calls → natural-language answers          |
| Chat UI *(TBD)*  | Streamlit or simple CLI      | End-user interface                                                      |

---

## 2. Dataset note

The public **Online Retail II** dataset from UCI provides transaction logs.  
The ZIP contains two CSVs covering **Dec 2009 → Dec 2010** (13 calendar months).  

Despite the file naming (`…2010_2011.csv`), there are **no 2011 rows**.  
This is why our KPI tests assert `months >= 13`.

---

## 3. Quick start

### Prerequisites
- Docker + Docker Compose
- Python **3.11 or 3.12**
- Poetry **1.8+**

### Setup (local dev)

```bash
# Clone
git clone https://github.com/rkendev/conversational-bi-assistant.git
cd conversational-bi-assistant

# Start services (Postgres + pgAdmin)
docker compose up -d db

# Install deps
poetry install

# Configure connection (default CI=5432, local=5433)
cp .env.example .env
# edit .env:
# POSTGRES_URL=postgresql+psycopg2://bi_user:bi_pass@localhost:5433/retail

# Ingest dataset (takes ~1 min)
poetry run python ingest.py --csv data/raw/online_retail_II*.csv

# Run agent demo
poetry run python agent.py
Run tests
bash
Copy code
poetry run pytest -q
All tests should pass (3 passed).

4. Ports & Environments
CI (GitHub Actions)
Uses Postgres on 5432 (default).
The workflow sets:

yaml
Copy code
env:
  POSTGRES_URL: postgresql+psycopg2://bi_user:bi_pass@localhost:5432/retail
Local dev
If another project already uses 5432, we map Postgres to 5433:

yaml
Copy code
services:
  db:
    ports:
      - "5433:5432"
With .env:

bash
Copy code
POSTGRES_URL=postgresql+psycopg2://bi_user:bi_pass@localhost:5433/retail
Thanks to python-dotenv, .env is loaded automatically in ingest.py, agent.py, and tests.

5. Folder structure
bash
Copy code
+-- data/                  # raw CSVs live here (git-ignored)
+-- ingest.py              # ETL – loads CSV → dimensional model
+-- scripts/
¦   +-- 01_create_views.sql    # KPI views (monthly revenue, top customers)
+-- mcp_server/            # Postgres MCP config + Dockerfile
+-- agent.py               # LangChain agent
+-- tests/                 # pytest suite
+-- docker-compose.yml     # Postgres + pgAdmin (MCP server later)
6. Roadmap
Week	Milestone
0 ✔︎	Repo scaffold, dataset ingest, KPI views, CI pipeline
1	Containerised Postgres MCP server & Compose update
2	LangChain Tool that calls MCP; basic Q&A in CLI
3	Streamlit chat UI, charts for numeric answers
4	Medium article + demo GIF; GitHub README badges

© 2025 rken · MIT License