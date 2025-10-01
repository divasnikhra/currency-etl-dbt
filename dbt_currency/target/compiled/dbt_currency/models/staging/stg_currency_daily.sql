

select
    fetch_date,
    country,
    currency,
    amount,
    currency_code,
    rate
from "postgres"."msd_financial_dbt"."currency_daily"
where rate is not null