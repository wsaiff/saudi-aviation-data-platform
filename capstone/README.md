# Saudi Aviation Infrastructure & Data Platform

> **Four datasets, one trusted view.** A modern data engineering pipeline and interactive platform focusing exclusively on Saudi Arabia's aviation infrastructure.

---

## 🚀 The Problem & Solution
Airport infrastructure data is traditionally scattered across separate source files (`airports.csv`, `runways.csv`, `navaids.csv`, `airport-frequencies.csv`)[cite: 10]. A planning analyst has to check multiple files before getting a complete picture[cite: 10]. 

This project solves the problem by building an end-to-end automated ELT pipeline (Python, BigQuery, dbt, Streamlit) that extracts raw OurAirports data, transforms and tests it through Bronze, Silver, and Gold layers, and serves a trusted, unified analytical dashboard[cite: 12].

---

## 📊 Key Features & Reporting
Our reporting helps stakeholders understand:
1. **Airport Infrastructure:** What infrastructure (runways, navaids, communication frequencies) is available at each Saudi airport[cite: 11]?
2. **Regional Comparison:** How airport infrastructure differs across Saudi administrative regions[cite: 11]?
3. **Data Coverage & Gaps:** Clear visibility into source-data coverage gaps without confusing missing records with missing physical infrastructure[cite: 5, 11].
