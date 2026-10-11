# Architecture

## System context
Current proposal for the Saudi Aviation Infrastructure & Data Platform; update the diagram as implementation and source access are confirmed.

```text
[ OurAirports Open Data ] 
       │ (raw extract)
       ▼
[ Daily Batch Pipeline ] (Python / Ingestion)
       │ (validated daily records)
       ▼
[ Warehouse / Local Storage ] 
       │ 
       ├──► [ Analytics & dbt Layers ] ──► [ Streamlit Dashboard ]
       │                                            ▲
       └────────────── [ Dashboard Stakeholder ] ───┘ (uses)
