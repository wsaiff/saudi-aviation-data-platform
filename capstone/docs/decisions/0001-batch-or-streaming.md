# ADR 0001: Batch or streaming

* **Status**: Accepted
* **Date**: 2026-10-11
* **Owners**: Data Engineering Team

## Context
The capstone project requires ingesting aviation data from our designated data sources into a local warehouse/storage layer to power our analytics and Streamlit dashboard. We need to decide whether to implement a batch-processing ingestion pipeline or a streaming architecture.

## Decision
We will use a **daily batch ingestion and processing approach** for our data pipeline. 

Given that the source data (OurAirports open datasets) is updated periodically rather than streamed in real-time, batch processing fits the project scope cleanly, keeps infrastructure complexity manageable, and ensures reliable daily runs for our dbt models and dashboard.

## Consequences
* **Simplicity & Reliability**: Easier to debug, test, and rerun pipeline tasks during development and evaluation.
* **Reproducibility**: Local CSV extracts and partitioned ingestion dates make it straightforward to demonstrate pipeline execution to instructors and reviewers.
* **No Real-Time Claims**: The dashboard will clearly reflect daily-updated operational metrics rather than live streaming telemetry, aligning correctly with project data availability.
