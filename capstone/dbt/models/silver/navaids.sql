select
    id as navaid_id,
    ident as navaid_ident,
    name as navaid_name,
    type as navaid_type,
    frequency_khz,
    latitude_deg,
    longitude_deg,
    elevation_ft,
    dme_frequency_khz,
    dme_channel,
    usageType as usage_type,
    associated_airport as associated_airport_ident,
    associated_airport is not null as has_airport_link
from {{ source('bronze', 'navaids') }}
where iso_country = 'SA'
