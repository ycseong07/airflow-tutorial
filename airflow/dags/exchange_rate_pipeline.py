# 외부 api로부터 파일을 받아 클리닝한 후 내 메일로 보내는 dag

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from hooks.clean_data import CleanDataHook

def use_clean_data_hook():
    hook = CleanDataHook()
    hook.clean_data()

# Define or Instantiate DAG
dag = DAG(
    'exchange_rate_etl',
    start_date=datetime(2023, 10, 1),
    end_date=datetime(2023, 12, 31),
    schedule_interval='0 22 * * *',
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    catchup=False
)

# Define or Instantiate Tasks
download_task = BashOperator(
    task_id='download_file',
    bash_command='curl -o xrate.csv https://data-api.ecb.europa.eu/service/data/EXR/M.USD.EUR.SP00.A?format=csvdata',
    cwd='/tmp',
    dag=dag,
)

clean_data_task = PythonOperator(
    task_id='clean_data',
    python_callable=use_clean_data_hook,
    dag=dag,
)

send_email_task = EmailOperator(
    task_id='send_email',
    to='ycseong07@gmail.com',
    subject='Exchange Rate Download - Successful',
    html_content='The Exchange Rate data has been successfully downloaded, cleaned, and loaded.',
    dag=dag,
)

# Define Task Dependencies
download_task >> clean_data_task >> send_email_task