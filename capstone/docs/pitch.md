# Capstone pitch

## Problem

Working hypothesis: The aviation planning analyst and stakeholders need a consistent, reliable daily view of Saudi Arabia's airport infrastructure (including airports, runways, navaids, and frequencies), but the source data is currently scattered across separate files, and formatting or regional naming inconsistencies need explicit validation and mapping.

## Solution

Profile the OurAirports dataset (`airports.csv`, `runways.csv`, `navaids.csv`, `airport-frequencies.csv`), agree on its grain and data contract with stakeholders, and build a repeatable daily batch ELT pipeline (Python, BigQuery, dbt) with an explicit dashboard-facing contract. The dashboard and its measures should follow validated stakeholder requirements rather than assumptions made from raw filenames.

## Rabbit holes

* Streaming before a freshness requirement is known.
* Inferring source semantics or keys from column names alone.
* Building dashboard measures before agreeing on their business meaning.
* Optimizing for volume or latency before measuring either.

## No-gos

* Committing raw or sensitive extracts.
* Treating unprofiled fields, keys, or freshness targets as confirmed facts.
* Presenting the daily output as real-time data.
