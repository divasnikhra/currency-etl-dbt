{{ config(
    materialized='table'
) }}

with daily as (
    select *
    from {{ ref('stg_currency_daily') }}
),

agg as (
    select
        extract(isoyear from fetch_date)::int as iso_year,
        extract(week from fetch_date)::int as iso_week,
        currency_code,
        avg(rate)::numeric(18,8) as avg_rate,
        count(*) as sample_count,
        min(fetch_date) as week_start_date
    from daily
    group by 1,2,3
)

select *
from agg
