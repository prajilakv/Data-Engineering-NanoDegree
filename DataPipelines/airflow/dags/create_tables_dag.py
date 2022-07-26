from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
#from udac_example_dag import default_args

default_args = {
    'owner': 'udacity',
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False
}

with DAG('create_table_dag', 
         start_date=datetime.now(),
         default_args=default_args) as dag:
    
    PostgresOperator(
        task_id="create_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql='create_tables.sql'
    )