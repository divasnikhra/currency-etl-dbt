Currency ETL with dbt

This project provides an end-to-end ETL pipeline to fetch currency exchange rates from an API, load the data into Postgres, and transform it into analytics-ready tables using dbt.

Setup Instructions

1. Clone the repository

git clone <repo-url>
cd currency_pipeline


2. Run the ETL pipeline
Simply execute the batch script:

run_etl.bat

What the Batch File Does

The run_etl.bat script fully automates the pipeline by:

Creating a Python virtual environment (if not already present)

Activating the virtual environment

Installing all dependencies from requirements.txt

Running the Python fetcher (src/fetch_currency_api.py) to pull daily exchange rates and save them in dbt_currency/seeds/

Executing dbt seed to load raw data into Postgres

Running dbt run to build staging and analytics-ready models

Running dbt test to validate transformations

No manual virtual environment setup is required — the batch file handles everything.

Running the Python Script Manually (Optional)

Although the batch file handles ingestion automatically, you can also run the fetcher directly:

python src/fetch_currency_api.py --config config.yml

Configuration

The config.yml file contains:

API endpoint and key

Postgres connection details

Target currency list

Make sure to update these values before running the pipeline.

Example Workflow

Run run_etl.bat

The pipeline fetches the latest exchange rates from the API

Data is written to CSV in dbt_currency/seeds/ and then loaded into Postgres staging tables

dbt builds weekly aggregates

Data is ready for analytics and reporting
