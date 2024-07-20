from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from load_data import load_data
from transform_data import transform_data
from model_regressor import learn_model_regressor
from model_classifier import learn_model_classifier

default_args = {
    'owner': 'v-vasileva-3',
    'depends_on_past': False,
    'email': ['slavushkoy@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'MFDP',
    default_args=default_args,
    description='MFDP',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 7, 9),
    tags=['MFDP'],
)


load_data = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

transform_data = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

model_regressor = BranchPythonOperator(
    task_id='model_regressor',
    python_callable=learn_model_regressor,
    dag=dag,
)

model_classifier = PythonOperator(
    task_id='model_classifier',
    python_callable=learn_model_classifier,
    op_kwargs={'target_classes': ['adopt_in_month', 'adopt_in_quarter']},
    dag=dag,
)


load_data >> transform_data
transform_data >> model_regressor
transform_data >> model_classifier