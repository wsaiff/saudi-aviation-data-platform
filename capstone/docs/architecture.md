# Architecture

## System context
Current proposal for the Saudi Aviation Infrastructure & Data Platform; update the architecture flow as implementation and source access are confirmed. The daily batch choice is recorded in [ADR 0001](./decisions/0001-daily-batch.md).

---

## Core Pipeline Flow

1. **Source Layer (`OurAirports`)**: Extracts raw open-source CSV datasets (airports, runways, navaids, frequencies, countries, and regions).
2. **Ingestion & Processing Layer (`Python`)**: Validates, cleans, and filters raw records strictly for Saudi airspace (`iso_country == 'SA'`).
3. **Data Warehouse & dbt Layers**: Structures and tests data to ensure a single, trusted analytical view.
4. **Presentation Layer (`Streamlit Dashboard`)**: Delivers interactive geospatial maps and infrastructure insights to stakeholders and aviation analysts.

---

## Open Decisions
* Source delivery and access mechanisms.
* Warehouse technology scaling.
* Runtime orchestration and scheduling.
* Reporting timezone and dashboard freshness targets.
