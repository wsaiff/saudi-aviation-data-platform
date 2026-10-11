# 🏗️ Architecture Design: Saudi Aviation Infrastructure & Data Platform

## 📊 System Context & Pipeline Flow (C2)

The platform follows a robust **ELT (Extract, Load, Transform)** architecture, separating raw data ingestion from analytical processing and geospatial visualization.

```mermaid
graph LR
    Source[OurAirports] -->|raw extract CSV| Pipeline[Python Batch Pipeline]
    Pipeline -->|validated Saudi records| Warehouse[Warehouse]
    Warehouse --> dbt[dbt & Analytics]
    dbt --> Dashboard[Streamlit Dashboard]
    Stakeholder[Stakeholder] -->|uses| Dashboard
