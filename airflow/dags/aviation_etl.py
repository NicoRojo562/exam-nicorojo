from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from scripts.load_data import create_database, create_table, insert_data

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "aviation_etl",
    default_args=default_args,
    schedule_interval=None,  # due to limited free requests to API (100)
    catchup=False,          
)

"""
3-step process to ensure correct execution of the pipe.
"""

# First check database
create_db_task = PythonOperator(
    task_id="create_db",
    python_callable=create_database,
    dag=dag,
)

# Then check table
create_table_task = PythonOperator(
    task_id="create_table",
    python_callable=create_table,
    dag=dag,
)

# Finally insert data
run_etl = PythonOperator(
    task_id="run_etl",
    python_callable=insert_data,
    dag=dag,
)

# Execution order
create_db_task >> create_table_task >> run_etl
