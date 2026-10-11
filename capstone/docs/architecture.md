# Architecture Design: Saudi Aviation Infrastructure & Data Platform

## 1. High-Level Architecture Overview
The platform follows a modern **ELT (Extract, Load, Transform)** architectural pattern, separating raw data ingestion from analytical transformation and visualization.

```text
[ OurAirports Open Data ] 
       │ (Python / Requests)
       ▼
[ Bronze Layer ] (Raw CSVs & Staging)
       │ (dbt Transformations & Tests)
       ▼
[ Silver / Gold Layers ] (Cleaned, Standardized & Analytics-Ready)
       │ (Streamlit & Plotly)
       ▼
[ Interactive Dashboard & Geospatial Maps ]
