{{ config(
    materialized='table'
) }}

select
    fetch_date,
    country,
    currency,
    amount,
    currency_code,
    rate
from {{ ref('currency_daily') }}
where rate is not null
