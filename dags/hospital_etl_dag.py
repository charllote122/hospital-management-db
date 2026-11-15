from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# 1. Define default arguments for the DAG
default_args = {
    "owner": "data_engineer",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,  # Retry 2 times if it fails
    "retry_delay": timedelta(minutes=1),  # Wait 1 minute between retries
}

# 2. Define the DAG
with DAG(
    "hospital_etl_pipeline",
    default_args=default_args,
    description="Runs the hospital Python ETL pipeline",
    schedule_interval=timedelta(days=1),  # Run once a day
    start_date=datetime(2026, 11, 1),
    catchup=False,  # Don't run for past dates immediately
    tags=["hospital", "etl"],
) as dag:

    # 3. Define the Tasks
    # Task 1: Check if the input files exist
    check_files = BashOperator(
        task_id="check_files",
        bash_command="ls /opt/airflow/python_scripts/data/raw/",
    )

    # Task 2: Run the Python ETL script
    run_etl = BashOperator(
        task_id="run_python_etl",
        # We explicitly pass the DB_HOST here so Docker knows to look at your Windows machine.
        # This overrides the .env file for this specific execution.
        bash_command="cd /opt/airflow/python_scripts && DB_HOST=host.docker.internal python main_etl.py",
    )

    # 4. Define the execution order (Dependencies)
    check_files >> run_etl
