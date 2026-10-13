with airports as (
    select * from {{ source('bronze', 'airports') }}
    where iso_country = 'SA'
),
regions as (
    select region_code, region_name from {{ ref('regions') }}
),
countries as (
    select code, name from {{ source('bronze', 'countries') }}
)
select
    a.id as airport_id,
    a.ident as airport_ident,
    a.type as airport_type,
    case a.type
        when 'large_airport' then 'Large'
        when 'medium_airport' then 'Medium'
        when 'small_airport' then 'Small'
    end as airport_size,
    a.name as airport_name,
    a.latitude_deg,
    a.longitude_deg,
    a.elevation_ft,
    a.iso_country as country_code,
    c.name as country_name,
    a.iso_region as region_code,
    r.region_name,
    a.municipality,
    a.scheduled_service = 'yes' as has_scheduled_service,
    a.icao_code,
    a.iata_code,
    a.type = 'closed' as is_closed,
    a.type = 'heliport' as is_heliport,
    a.type not in ('closed', 'heliport') as is_core,
    a.ident = 'AE-0001' as is_suspect_record
from airports a
left join regions r on a.iso_region = r.region_code
left join countries c on a.iso_country = c.code
