@echo off
REM ==============================================
REM Currency ETL - Full Run Script for Windows
REM ==============================================

REM 1. Check if venv exists, else create it
if not exist ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
)

REM 2. Activate Python virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate

REM 3. Upgrade pip and install dependencies
echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM 4. Run Python fetcher to get daily data
echo Fetching currency data from API...
python src\fetch_currency_api.py --config config.yml

REM 5. Change directory to dbt project
cd dbt_currency

REM 6. Run dbt seed to load CSV data
echo Loading seed data into Postgres...
dbt seed --profiles-dir .

REM 7. Run dbt models (staging + marts)
echo Running dbt models...
dbt run --profiles-dir .

REM 8. Optional: run dbt tests
echo Running dbt tests...
dbt test --profiles-dir .

REM 9. Return to root folder
cd ..

echo ETL run completed successfully!
pause
