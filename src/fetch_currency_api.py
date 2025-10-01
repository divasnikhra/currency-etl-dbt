import yaml
import pandas as pd
from datetime import date, timedelta
from dateutil import parser as date_parser
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests
from utils.logger import get_logger
from utils.exceptions import FetchError

logger = get_logger("fetcher")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), retry=retry_if_exception_type(FetchError))
def fetch_for_date(endpoint: str, d, lang: str = "EN", timeout: int = 10):
    date_str = d.strftime("%Y-%m-%d")
    url = f"{endpoint}?date={date_str}&lang={lang}"
    try:
        logger.info("Fetching %s", date_str)
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        payload = resp.json()
        return payload
    except Exception as e:
        logger.warning("Fetch failed for %s: %s", date_str, e)
        raise FetchError(e)

def run_fetch(config_path: str = "config.yml"):
    with open(config_path) as fh:
        cfg = yaml.safe_load(fh)

    api_cfg = cfg["api"]
    run_cfg = cfg["run"]

    # Generate dates
    if run_cfg["run_type"] == "daily":
        dates = [date.today()]
    else:
        start = date_parser.parse(run_cfg["start_date"]).date()
        end = date_parser.parse(run_cfg["end_date"]).date()
        dates = [start + timedelta(days=i) for i in range((end - start).days + 1)]

    all_rows = []
    for d in dates:
        payload = fetch_for_date(api_cfg["endpoint"], d, api_cfg.get("lang","EN"), timeout=api_cfg.get("timeout_seconds",10))
        for r in payload.get("rates", []):
            fetch_date_value = payload.get("date")
            if fetch_date_value is not None:
                fetch_date = pd.to_datetime(fetch_date_value).date()
            else:
                fetch_date = date.today()
            all_rows.append({
                "fetch_date": fetch_date,
                "country": r.get("country"),
                "currency": r.get("currency"),
                "amount": r.get("amount"),
                "currency_code": r.get("currencyCode"),
                "rate": float(str(r.get("rate")).replace(",", ".")) if r.get("rate") else None
            })

    df = pd.DataFrame(all_rows)
    import os
    os.makedirs("dbt_currency/seeds", exist_ok=True)
    df.to_csv("dbt_currency/seeds/currency_daily.csv", index=False)
    logger.info("Fetched %s rows", len(df))
    return df

if __name__ == "__main__":
    run_fetch()
