# Data Pipelines with Airflow

## Introduction

A music streaming company, Sparkify, wants to automate and monitor their data warehouse ETL pipelines using Apache Airflow.This project is to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

## Datasets
There are two datasets with the s3 link as below.

Log data: s3://udacity-dend/log_data
Song data: s3://udacity-dend/song_data

## Project Structure

Data Pipeline with Apache Airflow

|____dags
| |____ create_tables_dag.py   # DAG for creating tables on Redshift
| |____ create_tables.sql      # SQL CREATE queries
| |____ udac_example_dag.py    # Main DAG for this ETL data pipeline
|
|____plugins
| |____ __init__.py
| |
| |____operators
| | |____ __init__.py          # Define operators and helpers
| | |____ stage_redshift.py    # COPY data from S3 to Redshift
| | |____ load_fact.py         # Execute INSERT query into fact table
| | |____ load_dimension.py    # Execute INSERT queries into dimension tables
| | |____ data_quality.py      # Data quality check after pipeline execution
| |
| |____helpers
| | |____ __init__.py
| | |____ sql_queries.py       # SQL queries for building up dimensional tables

![image](https://user-images.githubusercontent.com/31400832/181036869-b6a3ef2e-42f1-4fb6-9394-7df1c858d6a9.png)

