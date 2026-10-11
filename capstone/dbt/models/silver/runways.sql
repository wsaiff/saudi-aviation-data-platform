select
    id as runway_id,
    airport_ident,
    le_ident,
    he_ident,
    length_ft,
    width_ft,
    surface as surface_source,
    case
        when surface is null then null
        when upper(trim(surface)) in ('ASP', 'ASPH', 'ASPHALT', 'BIT') then 'Asphalt'
        when upper(trim(surface)) in ('CON', 'CONCRETE') then 'Concrete'
        when upper(trim(surface)) = 'SAN' then 'Sand'
        when upper(trim(surface)) = 'EARTH' then 'Earth'
        when upper(trim(surface)) = 'UNK' then 'Unknown'
        else 'Other'
    end as surface_clean,
    lighted = 1 as is_lighted,
    closed = 1 as is_closed,
    le_elevation_ft,
    he_elevation_ft
from {{ source('bronze', 'runways') }}
where airport_ident in (select airport_ident from {{ ref('airports') }})
