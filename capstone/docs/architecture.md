# 🏗️ Architecture Design: Saudi Aviation Infrastructure & Data Platform

## 📊 System Context & Pipeline Flow (C2)

The platform follows a robust **ELT (Extract, Load, Transform)** architecture, separating raw data ingestion from analytical processing and geospatial visualization.

```mermaid
graph LR
    Source[OurAirports Open Data] -->|raw extract (CSV)| Pipeline[Daily Python Batch Pipeline]
    Pipeline -->|filtered & validated Saudi records| Warehouse[(Local/Cloud Warehouse)]
    Warehouse -->|dbt & Analytics Models| Dashboard[Streamlit Interactive Dashboard]
    Stakeholder[Aviation Analysts & Stakeholders] -->|uses & explores| Dashboard
