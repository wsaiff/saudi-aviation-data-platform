select
    code as region_code,
    name as region_name_source,
    case name
        when 'Jlzan Region' then 'Jazan Region'
        when 'Al Batah Region' then 'Al Bahah Region'
        else name
    end as region_name
from {{ source('bronze', 'regions') }}
where iso_country = 'SA'
