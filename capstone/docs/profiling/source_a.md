# Source A profiling report

**Status:** Not yet profiled  
**Input:** `data/source_a.csv` (expected local extract; not committed)  
**Owner:** TODO

Run [01_profile_source_a.ipynb](../../notebooks/01_profile_source_a.ipynb) on a
representative extract, then replace each TODO with observed results and the
sample window. Do not publish a contract based only on a partial or synthetic
sample.

## Findings

- **Grain:** TODO; describe what one row represents.
- **Candidate key:** TODO; include null and duplicate counts and the evidence
  used to accept or reject the key.
- **Nulls:** TODO; report material null rates and accepted exceptions.
- **Coverage:** TODO; include date range, missing periods, and timezone.
- **Surprises:** TODO; note unexpected values, duplicates, schema drift, or
  other anomalies.
- **Decisions:** TODO; link decisions to owners and follow-up actions.

## Contract updates

TODO: Record which findings changed `contracts/source_a.yml` and when the
source owner confirmed them.