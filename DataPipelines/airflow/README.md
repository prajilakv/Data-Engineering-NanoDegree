# Data Pipelines with Airflow

## Introduction

A music streaming company, Sparkify, wants to automate and monitor their data warehouse ETL pipelines using Apache Airflow.This project is to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

## Datasets
There are two datasets with the s3 link as below.

Log data: s3://udacity-dend/log_data
Song data: s3://udacity-dend/song_data

## Project Structure

### File Structure

1. dags
 - create_tables_dag.py   # DAG for creating tables 
 - create_tables.sql      # CREATE queries
 - udac_example_dag.py    # Main DAG 
 
2. plugins
 - __init__.py
 1. operators
 - __init__.py          
 - stage_redshift.py    # COPY data from S3 to Redshift
 - load_fact.py         # INSERT query into fact table
 - load_dimension.py    # INSERT queries into dimension tables
 -  data_quality.py     # Data quality check after pipeline execution
 2. helpers
 - __init__.py
 - sql_queries.py       # SQL queries 

### DAG Graph view

![image](https://user-images.githubusercontent.com/31400832/181036869-b6a3ef2e-42f1-4fb6-9394-7df1c858d6a9.png)

