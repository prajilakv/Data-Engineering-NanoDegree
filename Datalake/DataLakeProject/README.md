# Data Lake Project

## Introduction

A music streaming startup, Sparkify, has grown their user base and song database even more and want to move their data warehouse to a data lake. 
Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## Project Description

In this project, applying the knowlwdge on Spark and data lakes to build an ETL pipeline for a data lake hosted on S3. Data is loaded from S3, process the data 
into analytics tables using Spark, and load them back into S3. 

## Datasets 
There are two datasets namely log_data and song_data in the JSON format. They are retrieved from the s3 bucket.

## Schema
The tables created include one fact table, songplays and four dimensional tables namely users, songs, artists and time.

## Files

### etl.py
This retrieves the song and log data in the s3 bucket, transforms the data into fact and dimensional tables and loads the table data back into s3 as parquet files.

### dl.cfg
This contains AWS keys.

## To Execute

In the terminal, need to enter the below command

> python etl.py
