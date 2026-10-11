# Capstone pitch

## Problem
Working hypothesis: the dashboard stakeholder needs a consistent daily view of Saudi aviation infrastructure records, but scattered dataset files (airports, runways, navaids, and frequencies) make a unified view unclear, and reporting requirements still need confirmation.

## Solution
Profile the OurAirports open-source datasets, agree on their grain and data contract with teammates, then build a repeatable daily batch pipeline filtering strictly for Saudi airspace (`iso_country == 'SA'`) with an explicit dashboard-facing contract. The dashboard and its measures should follow validated stakeholder requirements, not assumptions made from a filename.

## Rabbit holes
* Streaming before a freshness requirement is known.
* Inferring source semantics or keys from column names alone.
* Building dashboard measures before agreeing on their business meaning.
* Optimizing for volume or latency before measuring either.

## No-gos
* Committing raw or sensitive extracts.
* Treating unprofiled fields, keys, or freshness targets as confirmed facts.
* Presenting the daily output as real-time data.
