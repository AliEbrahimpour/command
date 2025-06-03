from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import logging
logging.basicConfig(level=logging.DEBUG)
# Default arguments for the DAG


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 16),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create a DAG instance

dag = DAG(
    'sample_dag',
    default_args=default_args,
    description='A simple example DAG',
    schedule=timedelta(minutes=1),  # Run the DAG daily
)

# Define a Python function to be executed as a task
def print_hello():
    print("Hello, Airflow!")

# Create a PythonOperator task
task_hello = PythonOperator(
    task_id='task_hello',
    python_callable=print_hello,
    dag=dag,
)

# Set task dependencies (if any)
# task_hello >> [other_tasks]

# You can add more tasks here...

# Define the task order/dependencies (if any)
# For example: task_hello >> [other_tasks]

# Set up the task execution order/dependencies (if any)
task_hello

# You can add more tasks here...
