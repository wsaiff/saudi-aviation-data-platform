# Capstone pitch

## Problem

Working hypothesis: the dashboard stakeholder needs a consistent daily view of
aviation records, but the source, current reporting process, and decision being
made from the dashboard still need confirmation.

## Solution

Profile Source A, agree its grain and data contract with its owner, then build a
repeatable daily batch output with an explicit dashboard-facing contract. The
dashboard and its measures should follow validated stakeholder requirements,
not assumptions made from a filename.

## Rabbit holes

- Streaming before a freshness requirement is known.
- Inferring source semantics or keys from column names alone.
- Building dashboard measures before agreeing on their business meaning.
- Optimizing for volume or latency before measuring either.

## No-gos

- Committing raw or sensitive extracts.
- Treating unprofiled fields, keys, or freshness targets as confirmed facts.
- Presenting the daily output as real-time data.