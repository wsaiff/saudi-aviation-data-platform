# 🇸🇦 Saudi Aviation Infrastructure & Data Platform

## 🎯 Overview
An automated data engineering and analytics platform designed to provide a single, trusted view of aviation infrastructure across the Kingdom of Saudi Arabia. The platform consolidates scattered airport data sources—including locations, runways, navaids, and communication frequencies—into unified, high-quality analytical layers to support informed planning and decision-making.

---

## 🚀 Core Objectives
* 🔗 **Unified Infrastructure View**: Combine separate dataset files (airports, runways, navaids, and frequencies) into one cohesive source of truth for Saudi aviation.
* 📊 **Data Transparency & Coverage**: Identify available infrastructure, compare regional coverage, and highlight data gaps to assist stakeholders and analysts.
* ⚙️ **Automated ELT Pipeline**: Seamlessly extract, load, and transform open-source data to feed interactive dashboards and geospatial maps.

## Dashboard
The Streamlit dashboard entry point is `capstone/dashboard/app.py`. Run it from the repository root:

```bash
streamlit run capstone/dashboard/app.py
```

The Overview, Airport explorer, Data coverage, and About & sources pages are in `capstone/dashboard/pages/`.
