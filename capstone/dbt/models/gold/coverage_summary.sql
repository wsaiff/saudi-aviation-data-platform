with base as (
    select * from {{ ref('airport_infrastructure') }}
),
segments as (
    select 'By type' as segment_group, airport_type as segment,
           has_runway_data, has_frequency_data, has_navaid_data from base
    union all
    select 'Overall', 'All airports',
           has_runway_data, has_frequency_data, has_navaid_data from base
    union all
    select 'Overall', 'Core airports (no heliport/closed)',
           has_runway_data, has_frequency_data, has_navaid_data from base where is_core
)
select
    segment_group,
    segment,
    count(*) as airports,
    countif(has_runway_data) as with_runways,
    countif(has_frequency_data) as with_frequencies,
    countif(has_navaid_data) as with_navaids,
    round(100 * safe_divide(countif(has_runway_data), count(*)), 1) as pct_runways,
    round(100 * safe_divide(countif(has_frequency_data), count(*)), 1) as pct_frequencies,
    round(100 * safe_divide(countif(has_navaid_data), count(*)), 1) as pct_navaids
from segments
group by segment_group, segment
