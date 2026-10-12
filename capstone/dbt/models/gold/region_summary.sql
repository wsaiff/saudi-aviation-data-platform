select
    r.region_code,
    r.region_name,
    count(a.airport_ident) as total_airports,
    countif(a.is_core) as core_airports,
    countif(a.is_heliport) as heliports,
    countif(a.is_closed) as closed_airports,
    countif(a.has_runway_data) as airports_with_runways,
    countif(a.has_frequency_data) as airports_with_frequencies,
    countif(a.has_navaid_data) as airports_with_navaids,
    coalesce(sum(a.runway_count), 0) as total_runways
from {{ ref('regions') }} r
left join {{ ref('airport_infrastructure') }} a on r.region_code = a.region_code
group by r.region_code, r.region_name
