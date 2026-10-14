
FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DBT_PROFILES_DIR=/app/capstone/dbt

COPY capstone/ /app/capstone/

# Install project dependencies from pyproject.toml
WORKDIR /app/capstone
RUN pip install --no-cache-dir .

# Run Streamlit from the dashboard directory
WORKDIR /app/capstone/dashboard

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
