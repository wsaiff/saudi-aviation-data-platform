# Saudi Aviation Infrastructure & Data Platform

## Overview
An automated data engineering and analytics platform designed to collect, process, and analyze aviation infrastructure datasets specifically within the Kingdom of Saudi Arabia. The system automates raw data extraction from global aviation sources, performs data profiling, filters for Saudi airspace, and prepares structured datasets for advanced analytical operations and geospatial visualization.

---

## Core Objectives
* **Automated Data Ingestion**: Seamlessly retrieve daily updated aviation datasets (airports, runways, navaids, frequencies, and regional boundaries) from open-source repositories.
* **Data Profiling & Quality Control**: Inspect dataset schemas, detect missing values, and validate data integrity before execution.
* **Targeted Filtering**: Isolate and process records corresponding strictly to the Kingdom of Saudi Arabia (`iso_country == 'SA'`).
* **Downstream Analytics**: Deliver clean, standardized datasets ready for data warehousing and interactive dashboard integration.
