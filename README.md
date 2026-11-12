# TrendScope: Big Data-Based Internet Trend and Content Analytics System

## 1. System Overview

TrendScope is a distributed big data analytics platform designed to ingest, process, and analyze multi-regional video trend datasets. The system integrates the Apache Hadoop ecosystem (HDFS, Python Hadoop Streaming MapReduce, Apache Hive) with a Python-based processing pipeline, VADER Natural Language Processing, and an interactive analytics web dashboard.

### Core Technologies
- Programming Language: Python 3.10+
- Distributed Storage: Apache Hadoop HDFS 3.3+
- Distributed Processing: Python Hadoop Streaming (MapReduce)
- Data Warehouse: Apache Hive 3.1+ (HiveQL, ORC Storage)
- Data Processing: Pandas, NumPy
- Natural Language Processing: VADER Sentiment Analysis, Regex Tokenizer, N-Gram Modeling
- Visualization: Plotly, Matplotlib, WordCloud
- Web Application: Streamlit
- Containerization: Docker

---

## 2. System Architecture

```
[Ingestion Layer]
    |
    v
YouTube Trending Multi-Country Datasets (US, IN, GB, CA, FR) + Category Metadata JSON
    |
    v
[Storage Layer]
    |
    v
Hadoop Distributed File System (HDFS: /trendscope/raw/)
    |
    +---------------------------------------+
    |                                       |
    v                                       v
[Processing Layer - MapReduce]          [Data Warehouse Layer - Hive]
- Job 1: Keyword Frequency Analysis     - Database: trendscope
- Job 2: Category Statistics Aggregator  - Partitioned ORC Tables (by country)
- Job 3: Trending Persistence Analysis  - Windowed Analytical HiveQL Queries
    |                                       |
    +-------------------+-------------------+
                        |
                        v
[Serving & Visualization Layer]
Streamlit Web Interface + VADER Sentiment Engine + Plotly Visualizations
```

---

## 3. Directory Layout

```
TrendScope/
|-- .streamlit/
|   `-- config.toml
|-- data/
|   |-- raw/
|   |   |-- USvideos.csv
|   |   |-- INvideos.csv
|   |   |-- GBvideos.csv
|   |   |-- CAvideos.csv
|   |   |-- FRvideos.csv
|   |   |-- US_category_id.json
|   |   |-- IN_category_id.json
|   |   |-- GB_category_id.json
|   |   |-- CA_category_id.json
|   |   `-- FR_category_id.json
|   `-- processed/
|       |-- mapreduce_job1_keywords.csv
|       |-- mapreduce_job2_category_stats.csv
|       |-- mapreduce_job3_persistence.csv
|       |-- hive_top_channels.csv
|       `-- hive_regional_summary.csv
|-- mapreduce/
|   |-- job1_keyword_frequency/
|   |   |-- mapper.py
|   |   |-- reducer.py
|   |   `-- run_job.sh
|   |-- job2_category_stats/
|   |   |-- mapper.py
|   |   |-- reducer.py
|   |   `-- run_job.sh
|   |-- job3_trending_persistence/
|   |   |-- mapper.py
|   |   |-- reducer.py
|   |   `-- run_job.sh
|   `-- run_all_mapreduce_local.sh
|-- hive/
|   |-- create_tables.hql
|   |-- load_data.hql
|   |-- analytical_queries.hql
|   `-- run_hive_queries.sh
|-- scripts/
|   |-- generate_sample_data.py
|   |-- hadoop_pipeline.py
|   |-- run_hadoop_local.sh
|   |-- generate_report_pdf.py
|   `-- package_zip.py
|-- src/
|   |-- __init__.py
|   |-- data_loader.py
|   |-- nlp_engine.py
|   |-- analytics_engine.py
|   |-- hadoop_bridge.py
|   `-- ui_components.py
|-- tests/
|   |-- test_data_loader.py
|   |-- test_nlp_engine.py
|   |-- test_analytics.py
|   `-- test_mapreduce.py
|-- app.py
|-- Dockerfile
|-- render.yaml
|-- Procfile
|-- requirements.txt
|-- .gitignore
|-- TrendScope_Report.pdf
`-- README.md
```

---

## 4. Local Installation and Setup

### Prerequisites
- Python 3.10 or higher
- Git

### Step-by-Step Installation

```bash
# 1. Clone or extract repository
git clone https://github.com/your-username/TrendScope.git
cd TrendScope

# 2. Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install required Python packages
pip install -r requirements.txt

# 4. Start the Streamlit application
streamlit run app.py
```

The application runs at `http://localhost:8501`.

---

## 5. Big Data Pipeline Execution

### Local MapReduce Execution
To run all three MapReduce jobs locally using standard input/output pipes without a running Hadoop cluster:

```bash
bash mapreduce/run_all_mapreduce_local.sh
```

### Production Hadoop Cluster Execution
When connected to an active Hadoop cluster with HDFS:

```bash
# 1. Create HDFS directories and upload datasets
hdfs dfs -mkdir -p /trendscope/raw/
hdfs dfs -put data/raw/*.csv /trendscope/raw/

# 2. Execute MapReduce Job 1 (Keyword Frequency)
bash mapreduce/job1_keyword_frequency/run_job.sh

# 3. Execute MapReduce Job 2 (Category Statistics)
bash mapreduce/job2_category_stats/run_job.sh

# 4. Execute MapReduce Job 3 (Trending Persistence)
bash mapreduce/job3_trending_persistence/run_job.sh
```

### Apache Hive Ingestion and Analytical Queries

```bash
# Initialize database, load partitions, and execute analytical HiveQL queries
hive -f hive/create_tables.hql
hive -f hive/load_data.hql
hive -f hive/analytical_queries.hql
```

---

## 6. Docker Containerization

### Build Image
```bash
docker build -t trendscope:latest .
```

### Run Container
```bash
docker run -p 8501:8501 -e PORT=8501 trendscope:latest
```

---

## 7. Cloud Deployment

### Deploy on Render
1. Push repository to GitHub.
2. Log in to Render Dashboard.
3. Select **New -> Web Service**.
4. Configure service parameters:
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
5. Deploy service.

### Deploy on Koyeb
1. Connect GitHub repository in Koyeb Dashboard.
2. Select Dockerfile or Buildpack deployment.
3. Configure environment variable: `PORT=8000`.
4. Deploy service.

---

## 8. Test Suite Execution

Run all automated unit and integration tests:

```bash
python3 -m unittest discover tests
```
