from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from airflow.contrib.hooks.aws_hook import AwsHook

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 region="",
                 file_format="JSON",
                 json_path = '',                 
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.region= region
        self.file_format = file_format
        self.aws_credentials_id = aws_credentials_id
        self.execution_date = kwargs.get('execution_date')
        self.json_path = json_path
        
    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info("Deleting Redshift table.")
        redshift.run(f"DELETE FROM {self.table}")
        self.log.info("Copying")
        self.s3_key = self.s3_key.format(**context)
        s3_path = (f"s3://{self.s3_bucket}/{self.s3_key}")
        redshift.run(f"COPY {self.table} FROM '{s3_path}' ACCESS_KEY_ID '{credentials.access_key}' \
            SECRET_ACCESS_KEY '{credentials.secret_key}' FORMAT AS JSON '{self.json_path}'")





