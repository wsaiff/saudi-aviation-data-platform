# Bronze Layer Validation

## 1. Purpose

This document defines the validation procedures for the Bronze layer of the Saudi Aviation Infrastructure & Data Platform.

The Bronze layer stores raw aviation data ingested from OurAirports into Google BigQuery. Validation ensures that source data is loaded successfully, table structures are preserved, and ingestion failures are detected.

## 2. Scope

The Bronze layer contains six source tables:

| Table | Source |
|---|---|
| `airports` | [OurAirports airports.csv](https://davidmegginson.github.io/ourairports-data/airports.csv) |
| `runways` | [OurAirports runways.csv](https://davidmegginson.github.io/ourairports-data/runways.csv) |
| `navaids` | [OurAirports navaids.csv](https://davidmegginson.github.io/ourairports-data/navaids.csv) |
| `frequencies` | [OurAirports airport-frequencies.csv](https://davidmegginson.github.io/ourairports-data/airport-frequencies.csv) |
| `regions` | [OurAirports regions.csv](https://davidmegginson.github.io/ourairports-data/regions.csv) |
| `countries` | [OurAirports countries.csv](https://davidmegginson.github.io/ourairports-data/countries.csv) |

**Target:** Google BigQuery
**GCP project:** `saudi-aviation-infrastructure`
**Dataset:** `bronze`

> Ensure the project ID and dataset match the actual GCP environment configuration.

## 3. Validation Objectives

The following checks are performed on the Bronze layer:

1. **Table existence:** Confirm all six expected tables exist in BigQuery.
2. **Row counts:** Compare destination row counts with the source snapshot where possible.
3. **Schema validation:** Confirm expected source columns exist in the destination tables.
4. **Data type validation:** Inspect BigQuery column types and investigate unexpected changes.
5. **Data completeness:** Check that important fields are not unexpectedly empty.
6. **Loading reliability:** Confirm load jobs complete successfully, errors are reported, and repeated runs do not leave tables in an unexpected state.

## 4. Validation Procedure

### 4.1 Confirm Tables Exist

Run the following query in BigQuery:

```sql
SELECT
  table_name,
  creation_time
FROM
  `saudi-aviation-infrastructure.bronze.INFORMATION_SCHEMA.TABLES`
ORDER BY
  table_name;
```

**Expected result:** All six expected tables are listed.

### 4.2 Check Row Counts

```sql
SELECT 'airports' AS table_name, COUNT(*) AS row_count
FROM `saudi-aviation-infrastructure.bronze.airports`

UNION ALL

SELECT 'runways', COUNT(*)
FROM `saudi-aviation-infrastructure.bronze.runways`

UNION ALL

SELECT 'navaids', COUNT(*)
FROM `saudi-aviation-infrastructure.bronze.navaids`

UNION ALL

SELECT 'frequencies', COUNT(*)
FROM `saudi-aviation-infrastructure.bronze.frequencies`

UNION ALL

SELECT 'regions', COUNT(*)
FROM `saudi-aviation-infrastructure.bronze.regions`

UNION ALL

SELECT 'countries', COUNT(*)
FROM `saudi-aviation-infrastructure.bronze.countries`

ORDER BY table_name;
```

**Expected result:** All tables have plausible row counts. Compare counts against the corresponding source snapshot used for ingestion.

**Important:** OurAirports data changes over time, so comparing against a newly downloaded CSV may produce differences even when the original load was successful. Record the ingestion time and source counts whenever possible.

### 4.3 Inspect Schema and Data Types

```sql
SELECT
  table_name,
  column_name,
  ordinal_position,
  data_type,
  is_nullable
FROM
  `saudi-aviation-infrastructure.bronze.INFORMATION_SCHEMA.COLUMNS`
ORDER BY
  table_name,
  ordinal_position;
```

**Expected result:** All expected columns are present, and the BigQuery types are appropriate for the source data.

Review numeric coordinates, identifiers, timestamps, and other fields for unexpected type changes. Document intentional differences between source and destination types rather than assuming every CSV column must have the same type.

### 4.4 Check Required Values

Example: check airport identifiers.

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNTIF(ident IS NULL OR TRIM(ident) = '') AS missing_identifiers,
  COUNT(DISTINCT ident) AS distinct_identifiers
FROM
  `saudi-aviation-infrastructure.bronze.airports`;
```

This query provides a baseline for missing and distinct identifiers. Duplicate identifiers should be investigated in context rather than automatically treated as invalid, since the appropriate uniqueness rule depends on the data.

### 4.5 Validate Loading Reliability

For each ingestion run:

- Confirm the BigQuery load job completes successfully.
- Record the source table, destination table, loaded row count, execution time, and job status.
- Capture and report download, parsing, permission, and BigQuery errors.
- Confirm failed tables are visible in the final pipeline result.
- Test a repeated ingestion run and verify that it does not create duplicate records or leave unexpected data.
- Confirm a failed load does not silently appear successful or unnecessarily destroy a previously valid table.

The current ingestion implementation uses table loading with a configured write disposition. If it replaces destination tables, validate the source before replacement and verify that the completed load is successful.

## 5. Running the Validation Script

The validation script is maintained separately from ingestion in the `validation/` directory.

From the project root, run:

```bash
python -m validation.validate_bronze
```

The validator should inspect existing BigQuery tables without triggering ingestion or overwriting data.

Review the script output and investigate any failed checks or warnings.

## 6. Validation Results

**Validation method:** Manual verification using BigQuery SQL queries and inspection of the ingestion process.

**Validation date:** 2026-10-12

| Check | Status | Notes |
|---|---|---|
| All six tables exist | Passed | Verified manually in BigQuery. |
| Row counts reviewed | Passed | Counts checked using SQL queries. |
| Source and destination columns compared | Passed | Schema comparison completed. |
| BigQuery data types reviewed | Passed | Column types inspected in BigQuery. |
| Required-value checks completed | Passed | Required-value queries executed and reviewed. |
| Load job success verified | Passed | Ingestion results checked manually. |


**Overall result:** Manual Bronze validation completed. Follow-up automated validation and any outstanding reliability checks remain to be completed as indicated above.

| Check | Status | Notes |
|---|---|---|
| All six tables exist | Passed | |
| Row counts reviewed | Passed | |
| Source and destination columns compared | Passed | |
| BigQuery data types reviewed | Passed | |
| Required-value checks completed | Passed | |
| Load job success verified | Passed | |


Use `Passed`, `Failed`, or `Needs investigation` when recording actual results. Do not mark checks as passed until they have been executed.

## 7. Issues and Remediation

Record any issues found during validation.

| Date | Table | Issue | Action taken | Status |
|---|---|---|---|---|
| TBD | TBD | TBD | TBD | Pending |

Examples of issues include missing columns, unexpected data types, row-count discrepancies, permission errors, failed BigQuery jobs, and unexpected null values.

## 8. Completion Criteria

The Bronze layer is considered validated when:

- All expected tables exist.
- Row counts have been reviewed against the appropriate source snapshot.
- Column names and data types have been checked.
- Important missing-value checks have been reviewed.
- Ingestion job success and error handling have been verified.
- All discovered issues are resolved or explicitly documented.

## 9. Summary

Bronze validation establishes confidence that raw aviation data has been ingested into BigQuery and is available for downstream transformations. Silver and Gold layers will require additional validation for cleaning rules, data relationships, business logic, and analytical consistency.
