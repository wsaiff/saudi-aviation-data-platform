## Automated dbt Validation

**Validation date:** 2026-10-12

**Command executed:**

`dbt test --project-dir dbt --profiles-dir dbt`

**Result:** PASS

| Metric | Result |
|---|---:|
| Models discovered | 8 |
| Sources declared | 6 |
| Tests executed | 29 |
| Tests passed | 29 |
| Warnings | 0 |
| Errors | 0 |
| Skipped tests | 0 |
| Execution time | 16.13 seconds |

**Conclusion:** All 29 configured dbt data tests completed successfully. The tests covered required fields, uniqueness, accepted values, and relationships. No failures or warnings were reported.

This validates the configured data-quality rules against the relations tested. It does not establish that every possible data-quality issue has been covered. No model rebuild was performed by this `dbt test` command.
