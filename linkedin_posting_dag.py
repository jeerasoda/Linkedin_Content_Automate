from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago
import os
import random
from datetime import datetime, timedelta
import sys
sys.path.append('/opt/airflow/custom_modules')  # Fixed typo
from custom_modules.linkedin_generator import LinkedInAgentSystem
from custom_modules.azure_storage import AzureBlobStorage
from custom_modules.linkedin_api import LinkedinAPIClient

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'linkedin_posting_dag',
    default_args=default_args,
    description='A DAG to generate and post LinkedIn content',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    catchup=False,
) as dag:

    def generate_content():
        agent_system = LinkedInAgentSystem()
        content = agent_system.generate_content()
        return content

    def save_content_to_blob(**kwargs):
        content = kwargs['ti'].xcom_pull(task_ids='generate_content')
        blob_name = f"linkedin_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        azure_blob = AzureBlobStorage(blob_name)
        azure_blob.save_content(content)
        return blob_name

    def post_to_linkedin(**kwargs):
        blob_name = kwargs['ti'].xcom_pull(task_ids='save_content_to_blob')
        azure_blob = AzureBlobStorage(blob_name)
        content_data = azure_blob.get_content()
        linkedin_client = LinkedinAPIClient()
        response = linkedin_client.create_text_post(content_data['content'], visibility="PUBLIC")
        return response

    generate_content_task = PythonOperator(
        task_id='generate_content',
        python_callable=generate_content,
    )

    save_content_to_blob_task = PythonOperator(
        task_id='save_content_to_blob',
        python_callable=save_content_to_blob,
        provide_context=True,
    )

    post_to_linkedin_task = PythonOperator(
        task_id='post_to_linkedin',
        python_callable=post_to_linkedin,
        provide_context=True,
    )

    generate_content_task >> save_content_to_blob_task >> post_to_linkedin_task

