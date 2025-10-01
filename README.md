**Currency ETL with dbt**
This project implements an end-to-end ETL pipeline to fetch currency exchange rates from an API, load the raw data into Postgres, and transform it into analytics-ready tables using dbt.


**Setup Instructions**
1. Clone the repo

git clone <repo-url>
cd currency_pipeline

2. Run the ETL pipeline

Just run the batch script:
run_etl.bat

What the Batch File Does

The batch script (run_etl.bat) automates the entire process:

Creates a Python virtual environment automatically (if not already present).

Activates the virtual environment.

Installs all required dependencies from requirements.txt.

Runs the Python fetcher (src/fetch_currency_api.py) to get daily exchange rates and store them in dbt_currency/seeds/.

Runs dbt seed to load raw data into Postgres.

Runs dbt run to build staging and analytics-ready models.

Runs dbt test to validate the transformations.

No manual setup of virtual environment is needed — everything is handled inside the batch file.

Python Script (Optional Run)

The ingestion script is run automatically via the batch file, but you can run it manually if needed:

python src/fetch_currency_api.py --config config.yml

Configuration

config.yml contains:

API endpoint and key

Postgres connection details

Target currency list

Update this file before running the pipeline.

Example Workflow

Run run_etl.bat

Pipeline fetches latest exchange rates from API

Loads CSV into dbt_currency/seeds/ and then into Postgres staging

dbt builds weekly aggregates

Data is ready for downstream analytics
