select
    id as frequency_id,
    airport_ident,
    upper(trim(type)) as frequency_type,
    description,
    frequency_mhz
from {{ source('bronze', 'frequencies') }}
where airport_ident in (select airport_ident from {{ ref('airports') }})
