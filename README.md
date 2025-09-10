# Conversational BI Assistant 
*(LLM + Model Context Protocol + PostgreSQL)*

Ask business questions in plain English – the agent converts them to SQL through **MCP**, runs them on Postgres, and replies with concise insights.

---

## 1  What this project is

| Layer | Tech | Purpose |
|-------|------|---------|
| Data warehouse | **PostgreSQL 15** | Stores the Online Retail II dimensional model (`dim_product`, `dim_customer`, `fact_sales`) |
| Access layer | **Model Context Protocol (Postgres MCP server)** | Exposes the database schema & query endpoint to any LLM agent |
| Agent / Orchestration | **LangChain + Python 3.11** | Translates user prompts → MCP calls → natural-language answers |
| Chat UI *(TBD)* | Streamlit or simple CLI | End-user interface |

---

## 2  Dataset note

The public **“Online Retail II”** ZIP from UCI currently contains **two CSVs** that cover  
**December 2009 → December 2010** (13 calendar months).  
Despite the second file being named `…_2010_2011.csv`, **no 2011 rows are present**.

Our pipeline ingests both files and therefore creates **13 distinct `month` buckets** in the KPI views.

---

## 3  Quick-start

```bash
# 0) Clone & spin up services
git clone https://github.com/rkendev/conversational-bi-assistant.git
cd conversational-bi-assistant
docker compose up -d        # Postgres + pgAdmin

# 1) Download the data (≈ 25 MB each)
curl -L https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip -o data/raw/online_retail_II.zip
unzip data/raw/online_retail_II.zip -d data/raw/

```bash
# Prereqs: Docker, Python 3.12/3.11, Poetry 1.8+
cp .env.example .env  # or set POSTGRES_URL
docker compose up -d db mcp
poetry install --no-root
poetry run python ingest.py --csv data/raw/online_retail_II*.csv
poetry run python agent.py

# 2) Install Python deps
poetry install

# 3) Ingest → Postgres  (takes ~1½ min)
poetry run python ingest.py \
  --csv data/raw/online_retail_II.csv \
        data/raw/online_retail_II_2009_2010.csv
```
## 4 Smoke-test KPIs
pytest -q               # 2 tests - both should pass


## 5 Folder structure
```bash
+-- data/                # raw CSVs live here (git-ignored)
+-- ingest.py            # ETL – loads CSV ? dimensional model
+-- scripts/
¦   +-- 01_create_views.sql   # KPI views (monthly revenue, top customers)
+-- mcp_server/          # Postgres MCP config + Dockerfile (week 2)
+-- agent.py             # LangChain agent (week 3)
+-- tests/               # pytest suite
+-- docker-compose.yml   # Postgres + pgAdmin (MCP server added later)
```

## 6 Roadmap
Week	Milestone
0 ✔︎	Repo scaffold, dataset ingest, KPI views, CI
1	Containerised postgres-mcp-server & Compose update
2	LangChain Tool that calls MCP; basic Q&A in CLI
3	Streamlit chat UI, charts for numeric answers
4	Medium article + demo GIF; GitHub README badges

© 2025 rken · MIT License

