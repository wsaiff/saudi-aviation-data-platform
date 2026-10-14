# Gold Layer Validation

## 1. Purpose

This document records the manual data-quality validation performed on the Gold layer of the Saudi Aviation Infrastructure & Data Platform.

The objective is to ensure that analytics-ready aviation data is complete where required, logically valid, and consistent across airport infrastructure metrics, coverage summaries, and regional summaries before it is used by the dashboard and reporting layer.

## 2. Scope

**GCP project:** `saudi-aviation-infrastructure`
**BigQuery dataset:** `gold`
**Validation method:** Manual SQL queries executed in BigQuery
**Validation date:** Record the date the checks are executed

The validation covers three Gold tables:

| Table                    | Main validation areas                                                                       |
| ------------------------ | ------------------------------------------------------------------------------------------- |
| `airport_infrastructure` | Airport identifiers, infrastructure counts, completeness score, airport-size classification |
| `coverage_summary`       | Segment definitions, coverage counts, percentage calculations                               |
| `region_summary`         | Regional totals, airport classifications, infrastructure coverage, runway totals            |

Row counts should be recorded after running the validation queries. They may change when the source data or transformation logic is updated.

## 3. Validation Methodology

Two types of SQL checks are used:

- **Summary checks:** Return a row containing counts or aggregate values for review.

- **Issue-detection checks:** Return individual records that violate a specific rule. Zero returned rows means no violations were detected for that rule.


The checks are read-only and do not modify Gold tables.

The Gold models should reflect the latest Silver transformations before validation. Running `dbt test` alone does not rebuild the Gold models.

## 4. Validation Checks

### 4.1 Airport Infrastructure

**Checks performed:**

- Missing or blank `airport_ident`

- Missing `airport_id`

- Duplicate airport identifiers

- `data_completeness_score` outside the range 0–3

- Consistency between infrastructure counts and their Boolean flags

- Correct mapping of `airport_type` to `airport_size`

- Preservation of airports that have no associated runway, frequency, or navaid data


**Check A: Inspect row count and required fields**

```
SELECT
    COUNT(*) AS total_rows,
    COUNTIF(airport_id IS NULL) AS missing_airport_id,
    COUNTIF(
        airport_ident IS NULL OR TRIM(airport_ident) = ''
    ) AS missing_airport_ident
FROM `saudi-aviation-infrastructure.gold.airport_infrastructure`;
```

**Check B: Find duplicate or missing airport identifiers**

```
SELECT
    airport_ident,
    COUNT(*) AS record_count
FROM `saudi-aviation-infrastructure.gold.airport_infrastructure`
GROUP BY airport_ident
HAVING airport_ident IS NULL
    OR TRIM(airport_ident) = ''
    OR COUNT(*) > 1;
```

**Check C: Validate data-completeness scores**

```
SELECT
    airport_ident,
    data_completeness_score
FROM `saudi-aviation-infrastructure.gold.airport_infrastructure`
WHERE data_completeness_score IS NULL
   OR data_completeness_score NOT BETWEEN 0 AND 3;
```

**Check D: Validate infrastructure flags and counts**

```
SELECT
    airport_ident,
    runway_count,
    has_runway_data,
    frequency_count,
    has_frequency_data,
    navaid_count,
    has_navaid_data
FROM `saudi-aviation-infrastructure.gold.airport_infrastructure`
WHERE runway_count < 0
   OR frequency_count < 0
   OR navaid_count < 0
   OR has_runway_data IS DISTINCT FROM (runway_count > 0)
   OR has_frequency_data IS DISTINCT FROM (frequency_count > 0)
   OR has_navaid_data IS DISTINCT FROM (navaid_count > 0);
```

**Check E: Validate airport-size classification**

```
SELECT
    airport_ident,
    airport_type,
    airport_size
FROM `saudi-aviation-infrastructure.gold.airport_infrastructure`
WHERE
    (airport_type = 'large_airport'
        AND airport_size IS DISTINCT FROM 'Large')
    OR
    (airport_type = 'medium_airport'
        AND airport_size IS DISTINCT FROM 'Medium')
    OR
    (airport_type = 'small_airport'
        AND airport_size IS DISTINCT FROM 'Small');
```

**Expected results:**

- Airport identifiers should be populated and unique.

- Missing required IDs are investigated.

- Data-completeness scores should be integers between 0 and 3.

- Infrastructure flags should agree with their corresponding counts.

- Large, medium, and small airports should have the expected size labels.

- Null `airport_size` values for other airport types are reviewed according to the Silver transformation rules.


**Observed result:** Record after executing the queries.

### 4.2 Coverage Summary

**Checks performed:**

- Expected coverage segments are present.

- Airport counts and infrastructure counts are non-negative.

- Infrastructure counts do not exceed the total airport count for a segment.

- Coverage percentages are between 0 and 100.

- Coverage percentages agree with the underlying counts.

- Overall and core-airport summaries agree with `airport_infrastructure`.


**Check A: Inspect coverage segments**

```
SELECT
    segment_group,
    segment,
    airports,
    with_runways,
    with_frequencies,
    with_navaids,
    pct_runways,
    pct_frequencies,
    pct_navaids
FROM `saudi-aviation-infrastructure.gold.coverage_summary`
ORDER BY segment_group, segment;
```

**Check B: Find invalid counts or percentages**

```
SELECT *
FROM `saudi-aviation-infrastructure.gold.coverage_summary`
WHERE airports < 0
   OR with_runways < 0
   OR with_frequencies < 0
   OR with_navaids < 0
   OR with_runways > airports
   OR with_frequencies > airports
   OR with_navaids > airports
   OR pct_runways < 0 OR pct_runways > 100
   OR pct_frequencies < 0 OR pct_frequencies > 100
   OR pct_navaids < 0 OR pct_navaids > 100;
```

**Check C: Validate percentage calculations**

```
SELECT *
FROM `saudi-aviation-infrastructure.gold.coverage_summary`
WHERE
    pct_runways IS DISTINCT FROM
        ROUND(100 * SAFE_DIVIDE(with_runways, airports), 1)
    OR pct_frequencies IS DISTINCT FROM
        ROUND(100 * SAFE_DIVIDE(with_frequencies, airports), 1)
    OR pct_navaids IS DISTINCT FROM
        ROUND(100 * SAFE_DIVIDE(with_navaids, airports), 1);
```

**Check D: Compare overall segments against airport-level data**

```
WITH expected AS (
    SELECT
        'All airports' AS segment,
        COUNT(*) AS airports,
        COUNTIF(has_runway_data) AS with_runways,
        COUNTIF(has_frequency_data) AS with_frequencies,
        COUNTIF(has_navaid_data) AS with_navaids
    FROM `saudi-aviation-infrastructure.gold.airport_infrastructure`

    UNION ALL

    SELECT
        'Core airports (no heliport/closed)' AS segment,
        COUNT(*) AS airports,
        COUNTIF(has_runway_data) AS with_runways,
        COUNTIF(has_frequency_data) AS with_frequencies,
        COUNTIF(has_navaid_data) AS with_navaids
    FROM `saudi-aviation-infrastructure.gold.airport_infrastructure`
    WHERE is_core
)
SELECT
    e.segment,
    e.airports AS expected_airports,
    c.airports AS actual_airports,
    e.with_runways AS expected_with_runways,
    c.with_runways AS actual_with_runways,
    e.with_frequencies AS expected_with_frequencies,
    c.with_frequencies AS actual_with_frequencies,
    e.with_navaids AS expected_with_navaids,
    c.with_navaids AS actual_with_navaids
FROM expected e
LEFT JOIN `saudi-aviation-infrastructure.gold.coverage_summary` c
    ON c.segment_group = 'Overall'
   AND c.segment = e.segment
WHERE c.segment IS NULL
   OR e.airports IS DISTINCT FROM c.airports
   OR e.with_runways IS DISTINCT FROM c.with_runways
   OR e.with_frequencies IS DISTINCT FROM c.with_frequencies
   OR e.with_navaids IS DISTINCT FROM c.with_navaids;
```

**Expected results:**

- The `Overall` group contains `All airports` and `Core airports (no heliport/closed)`.

- `By type` segments correspond to airport types present in the input data.

- Counts are non-negative and do not exceed their segment totals.

- Percentages fall between 0 and 100 and match the calculated ratios.

- The overall and core-airport counts match the airport-level infrastructure data.


**Observed result:** Record after executing the queries. Zero rows from issue-detection queries indicate that no violations were detected by those checks.

### 4.3 Region Summary

**Checks performed:**

- Missing or blank `region_code`

- Duplicate region codes

- Negative regional counts or runway totals

- Infrastructure counts exceeding the relevant airport totals

- Consistency of regional aggregates with `airport_infrastructure`

- Regions with zero airports


**Check A: Find missing or duplicate region codes**

```
SELECT
    region_code,
    COUNT(*) AS record_count
FROM `saudi-aviation-infrastructure.gold.region_summary`
GROUP BY region_code
HAVING region_code IS NULL
    OR TRIM(region_code) = ''
    OR COUNT(*) > 1;
```

**Check B: Find invalid regional counts**

```
SELECT *
FROM `saudi-aviation-infrastructure.gold.region_summary`
WHERE total_airports < 0
   OR core_airports < 0
   OR heliports < 0
   OR closed_airports < 0
   OR airports_with_runways < 0
   OR airports_with_frequencies < 0
   OR airports_with_navaids < 0
   OR core_with_runways < 0
   OR core_with_frequencies < 0
   OR core_with_navaids < 0
   OR total_runways < 0
   OR core_airports > total_airports
   OR heliports > total_airports
   OR closed_airports > total_airports
   OR airports_with_runways > total_airports
   OR airports_with_frequencies > total_airports
   OR airports_with_navaids > total_airports
   OR core_with_runways > core_airports
   OR core_with_frequencies > core_airports
   OR core_with_navaids > core_airports;
```

**Check C: Reconcile regional totals with airport-level data**

```
WITH expected AS (
    SELECT
        region_code,
        COUNT(airport_ident) AS total_airports,
        COUNTIF(is_core) AS core_airports,
        COUNTIF(is_heliport) AS heliports,
        COUNTIF(is_closed) AS closed_airports,
        COUNTIF(has_runway_data) AS airports_with_runways,
        COUNTIF(has_frequency_data) AS airports_with_frequencies,
        COUNTIF(has_navaid_data) AS airports_with_navaids,
        COUNTIF(is_core AND has_runway_data) AS core_with_runways,
        COUNTIF(is_core AND has_frequency_data) AS core_with_frequencies,
        COUNTIF(is_core AND has_navaid_data) AS core_with_navaids,
        COALESCE(SUM(runway_count), 0) AS total_runways
    FROM `saudi-aviation-infrastructure.gold.airport_infrastructure`
    GROUP BY region_code
)
SELECT
    r.region_code,
    r.total_airports AS actual_total_airports,
    e.total_airports AS expected_total_airports,
    r.total_runways AS actual_total_runways,
    e.total_runways AS expected_total_runways
FROM `saudi-aviation-infrastructure.gold.region_summary` r
LEFT JOIN expected e
    ON r.region_code = e.region_code
WHERE e.region_code IS NULL
   OR r.total_airports IS DISTINCT FROM e.total_airports
   OR r.core_airports IS DISTINCT FROM e.core_airports
   OR r.heliports IS DISTINCT FROM e.heliports
   OR r.closed_airports IS DISTINCT FROM e.closed_airports
   OR r.airports_with_runways IS DISTINCT FROM e.airports_with_runways
   OR r.airports_with_frequencies IS DISTINCT FROM e.airports_with_frequencies
   OR r.airports_with_navaids IS DISTINCT FROM e.airports_with_navaids
   OR r.core_with_runways IS DISTINCT FROM e.core_with_runways
   OR r.core_with_frequencies IS DISTINCT FROM e.core_with_frequencies
   OR r.core_with_navaids IS DISTINCT FROM e.core_with_navaids
   OR r.total_runways IS DISTINCT FROM e.total_runways;
```

**Check D: Inspect regions with zero airports**

```
SELECT
    region_code,
    region_name,
    total_airports,
    total_runways
FROM `saudi-aviation-infrastructure.gold.region_summary`
WHERE total_airports = 0;
```

**Expected results:**

- Region codes should be populated and unique.

- Regional counts and runway totals should be non-negative.

- Infrastructure counts should not exceed the relevant airport totals.

- Regional aggregate values should match the airport-level data.

- Regions with zero airports are reviewed but are not automatically treated as errors, because the model starts with the Silver `regions` table and preserves regions through a left join.


**Observed result:** Record after executing the queries. Investigate any discrepancies before accepting the Gold results.

## 5. Summary of Results

Complete this table after running the validation queries.

| Validation area                     | Status | Notes                                    |
| ----------------------------------- | ------ | ---------------------------------------- |
| Gold table existence and row counts | Passed | Confirm all three tables are accessible  |
| Airport identifiers and uniqueness  | Passed | Check missing and duplicate identifiers  |
| Infrastructure flags and counts     | Passed | Confirm flags agree with counts          |
| Data-completeness score             | Passed | Confirm values are between 0 and 3       |
| Airport-size classification         | Passed | Confirm expected mappings                |
| Coverage summary counts             | Passed | Check segments and counts                |
| Coverage percentage calculations    | Passed | Confirm percentages match counts         |
| Overall coverage reconciliation     | Passed | Compare with airport-level data          |
| Region identifiers and uniqueness   | Passed | Check missing and duplicate region codes |
| Regional totals and runway counts   | Passed | Reconcile regional aggregates            |
| Regions with zero airports          | Passed | Review whether they are expected         |

These statuses should be updated based on the actual query results. They do not imply that every possible data-quality rule has been tested.

## 6. Findings and Remediation

Record any unexpected data-quality issues identified during validation.

For each issue, document:

- Affected Gold table and column.

- Validation rule that failed.

- Number of affected records.

- Root cause, if identified.

- Corrective action taken.

- Retest result.


Do not modify Gold data directly merely to make a validation query pass. Investigate whether the issue originates in source data, Silver transformations, Gold aggregation logic, or the validation assumptions.

## 7. Limitations

- Validation is performed manually using SQL queries.

- The checks cover selected completeness, uniqueness, range, aggregation, and consistency rules rather than every possible data-quality issue.

- Some null values and zero-count regions may be legitimate.

- The results depend on the current source data and transformation logic.

- The checks do not independently prove that every source record was ingested correctly.

- The checks have not yet been fully integrated into automated dbt tests.


## 8. Next Steps

1. Execute the validation queries and record the actual results.

2. Investigate and document any unexpected failures.

3. Convert confirmed validation rules into dbt data tests.

4. Add custom dbt tests for percentage calculations and aggregate reconciliation.

5. Rerun validation whenever relevant Silver or Gold models change.

6. Confirm that the Streamlit dashboard uses the intended Gold tables and interprets nulls and coverage metrics correctly.


## 9. Conclusion

The Gold layer provides analytics-ready airport infrastructure metrics, infrastructure coverage summaries, and regional aggregates.

Validation should confirm that the models preserve the intended airport and region populations, calculate infrastructure metrics consistently, and produce accurate coverage percentages and regional totals.

The Gold layer should be considered validated after the queries have been executed, unexpected issues have been resolved or documented, and the actual results have been recorded above.
