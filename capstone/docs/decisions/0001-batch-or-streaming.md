# ADR 0001: Batch or streaming

- **Status:** Proposed
- **Date:** TODO
- **Owners:** Product, Source, Platform

## Context

The capstone needs a repeatable path from Source A to a daily warehouse output
used by a dashboard. The source delivery mechanism, volume, and stakeholder
freshness requirement have not yet been confirmed.

## Decision

Start with batch ingestion and daily processing. Treat this as a reversible
capstone decision, not a claim about the source's capabilities. Revisit it when
the source owner confirms delivery options and the dashboard stakeholder sets
an acceptable freshness target.

## Consequences

- The first implementation can be rerun against a bounded extract and checked
  for reproducibility.
- The dashboard contract must state its reporting date and freshness target
  once those are agreed.
- Data may be stale between batch runs; the dashboard must not imply real-time
  coverage.
- A streaming design would add operational and data-quality complexity and is
  deferred unless the validated freshness requirement needs it.