# Saudi Aviation Data Platform Capstone

## Problem and stakeholder

Working hypothesis: an aviation dashboard stakeholder needs a consistent daily
view of records from Source A. Confirm the stakeholder, current pain point, and
decision the dashboard supports before finalizing scope; see
[the pitch](docs/pitch.md).

## Decision

The proposed first iteration uses daily batch processing. This is reversible
and pending confirmation of source delivery options and the stakeholder's
freshness requirement. See [the ADR](docs/decisions/0001-batch-or-streaming.md)
and [the architecture](docs/architecture.md).

## How to run

1. Put a representative, authorized extract at `data/source_a.csv`. Local data
   is ignored by Git.
2. Open `notebooks/01_profile_source_a.ipynb` in VS Code with the Jupyter
   extension and a Python environment containing `pandas`.
3. Run the cells in order, then record reviewed findings in
   [the profiling report](docs/profiling/source_a.md) and update
   `contracts/source_a.yml` only after the source owner confirms them.

The notebook is exploration only. Production code must not import from
`notebooks/`. Source and dashboard-facing draft contracts are in `contracts/`.
Replace placeholder GitHub teams in `.github/CODEOWNERS` before relying on
automatic reviewer assignment.