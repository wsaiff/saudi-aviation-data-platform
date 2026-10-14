# Silver Layer Validation

## 1. Purpose

This document records the manual data-quality validation performed on the Silver layer of the Saudi Aviation Infrastructure & Data Platform.

The objective is to ensure that cleaned and standardized aviation data is complete where required, logically valid, and consistent across related tables before it is used by the Gold layer.

## 2. Scope

**GCP project:** `saudi-aviation-infrastructure`
**BigQuery dataset:** `silver`
**Validation method:** Manual SQL queries executed in BigQuery
**Validation date:** 2026-10-12

The validation covers five Silver tables:

| Table | Rows observed | Main validation areas |
|---|---:|---|
| `airports` | 193 | Required fields, duplicate identifiers, coordinate ranges |
| `frequencies` | 157 | Positive frequency values, airport references |
| `navaids` | 54 | Required identifiers, coordinate ranges, airport associations |
| `regions` | 14 | Required region fields, duplicate region codes |
| `runways` | 95 | Required identifiers, non-negative dimensions, airport references |

Row counts represent the values observed during manual validation and may change if the source data or transformations are updated.

## 3. Validation Methodology

Two types of SQL checks were used:

- **Summary checks:** Return a row containing counts of missing or invalid values.
- **Issue-detection checks:** Return individual records that violate a specific rule. Zero returned rows means no violations were detected for that rule.

The checks are read-only and do not modify Silver tables.

## 4. Validation Checks

### 4.1 Airports

**Checks performed:**
- Missing `airport_id`
- Missing or blank `airport_ident`
- Missing or blank `airport_name`
- Latitude outside the range -90 to 90
- Longitude outside the range -180 to 180
- Duplicate non-empty `airport_ident` values
- Correct mapping of `airport_type` to the derived `airport_size` column.
- `airport_size` contains only `Large`, `Medium`, `Small`, or `NULL`.
- `NULL` values in `airport_size` are reviewed for airport types that are not included in the mapping.

**Expected results:**
- No invalid coordinate values
- No duplicate identifiers, if `airport_ident` is confirmed as unique under the project rules
- Missing required values are investigated
- Null sizes are consistent with the transformation rules and are not automatically treated as errors.

**Observed result:** Manual checks appeared to pass; no unexpected issues were reported.

### 4.2 Frequencies

**Checks performed:**
- Non-positive `frequency_mhz` values
- Non-empty `airport_ident` values that do not match an airport

**Expected results:**
- No non-positive frequency values
- No unexplained references to missing airports

**Observed result:** Manual checks appeared to pass; issue-detection queries returned no unexpected records.

### 4.3 Navaids

**Checks performed:**
- Missing `navaid_id`
- Missing or blank `navaid_ident`
- Latitude outside the range -90 to 90
- Longitude outside the range -180 to 180
- Non-empty associated airport identifiers that do not match an airport

**Expected results:**
- No invalid coordinate values
- Missing identifiers and unmatched airport references are investigated
- Missing airport associations are not automatically treated as errors

**Observed result:** Manual checks appeared to pass; no unexpected issues were reported.

### 4.4 Regions

**Checks performed:**
- Missing or blank `region_code`
- Missing or blank `region_name`
- Duplicate non-empty `region_code` values

**Expected results:**
- Region codes are populated and unique if required by the data model
- Missing region names are reviewed

**Observed result:** Manual checks appeared to pass; no unexpected issues were reported.

### 4.5 Runways

**Checks performed:**
- Missing `runway_id`
- Negative `length_ft`
- Negative `width_ft`
- Non-empty `airport_ident` values that do not match an airport

**Expected results:**
- No negative runway dimensions
- Missing identifiers and unmatched airport references are investigated
- Null or zero measurements are assessed according to the project rules

**Observed result:** Manual checks appeared to pass; issue-detection queries returned no unexpected records.

## 5. Summary of Results

| Validation area | Status | Notes |
|---|---|---|
| Silver table row counts | Reviewed | Five tables inspected |
| Airport identifiers and coordinates | Passed manually | No unexpected issues reported |
| Frequency values and airport references | Passed manually | No unexpected records reported |
| Navaid identifiers, coordinates, and airport associations | Passed manually | No unexpected issues reported |
| Region codes and names | Passed manually | No unexpected issues reported |
| Runway identifiers and dimensions | Passed manually | No unexpected issues reported |
| Runway-to-airport references | Passed manually | No unexpected records reported |

These statuses reflect the manual checks performed. They do not imply that every possible data-quality rule has been tested.

## 6. Findings and Remediation

No unexpected data-quality issues were identified during the initial manual validation.

No Silver data changes were required as a result of these checks.

If future validation reveals problems, record the affected table, issue, root cause, corrective action, and retest result in this section.

## 7. Limitations

- Validation was performed manually using SQL queries.
- The checks cover selected completeness, uniqueness, range, and relationship rules rather than every possible data-quality issue.
- Some missing values may be legitimate in aviation source data.
- The observed row counts can change when source data or transformation logic changes.
- The checks have not yet been integrated into automated dbt tests.

## 8. Next Steps

1. Convert confirmed validation rules into dbt data tests.
2. Add tests for required fields and uniqueness where justified by the data model.
3. Add custom tests for coordinate ranges, positive frequency values, and non-negative runway dimensions.
4. Investigate and document any future failures.
5. Rerun the tests whenever Silver models change.
6. Validate Gold models after Silver validation is automated.

## 9. Conclusion

Manual validation of the five Silver tables was completed. The initial checks appeared to pass, with no unexpected data-quality issues reported.

The next step is to automate the confirmed rules using dbt so that data-quality checks can be repeated consistently as the platform evolves.
