
FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DBT_PROFILES_DIR=/app/capstone/dbt

COPY capstone/pyproject.toml /app/capstone/pyproject.toml
COPY capstone/dashboard/requirements.txt /app/capstone/dashboard/requirements.txt

RUN pip install --no-cache-dir \
    -r /app/capstone/dashboard/requirements.txt \
    "dbt-bigquery>=1.9,<2.0" \
    "google-cloud-bigquery>=3.0" \
    "python-dotenv>=1.0" \
    "pyarrow>=14,<26" \
    "requests==2.34.2"

COPY capstone/ /app/capstone/

WORKDIR /app/capstone

EXPOSE 8501

CMD ["streamlit", "run", "dashboard/app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
