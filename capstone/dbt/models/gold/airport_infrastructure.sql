with airports as (
    select * from {{ ref('airports') }}
),
runway_stats as (
    select
        airport_ident,
        count(*) as runway_count,
        max(length_ft) as longest_runway_ft,
        string_agg(distinct surface_clean, ', ') as runway_surfaces
    from {{ ref('runways') }}
    group by airport_ident
),
frequency_stats as (
    select
        airport_ident,
        count(*) as frequency_count,
        string_agg(distinct frequency_type, ', ' order by frequency_type) as frequency_types
    from {{ ref('frequencies') }}
    group by airport_ident
),
navaid_stats as (
    select
        associated_airport_ident as airport_ident,
        count(*) as navaid_count,
        string_agg(distinct navaid_type, ', ' order by navaid_type) as navaid_types
    from {{ ref('navaids') }}
    where has_airport_link
    group by associated_airport_ident
),
joined as (
    select
        a.airport_id,
        a.airport_ident,
        a.airport_name,
        a.airport_type,
        a.airport_size,
        a.icao_code,
        a.iata_code,
        a.latitude_deg,
        a.longitude_deg,
        a.elevation_ft,
        a.region_code,
        a.region_name,
        a.municipality,
        a.has_scheduled_service,
        a.is_closed,
        a.is_heliport,
        a.is_core,
        coalesce(r.runway_count, 0) as runway_count,
        r.longest_runway_ft,
        r.runway_surfaces,
        coalesce(f.frequency_count, 0) as frequency_count,
        f.frequency_types,
        coalesce(n.navaid_count, 0) as navaid_count,
        n.navaid_types,
        coalesce(r.runway_count, 0) > 0 as has_runway_data,
        coalesce(f.frequency_count, 0) > 0 as has_frequency_data,
        coalesce(n.navaid_count, 0) > 0 as has_navaid_data
    from airports a
    left join runway_stats r on a.airport_ident = r.airport_ident
    left join frequency_stats f on a.airport_ident = f.airport_ident
    left join navaid_stats n on a.airport_ident = n.airport_ident
)
select
    *,
    cast(has_runway_data as int64)
      + cast(has_frequency_data as int64)
      + cast(has_navaid_data as int64) as data_completeness_score
from joined