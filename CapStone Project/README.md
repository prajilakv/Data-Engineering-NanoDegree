# Immigration Data Project

### Data Engineering Capstone Project

#### Project Summary
In this project I am working with I94 immigration dataset, which contains immigration data for U.S. ports to find immigration patterns to the US and find answers to the question like,

- During which month, from which country most people visite US?

The project follows the follow steps:
* Step 1: Scope the Project and Gather Data
* Step 2: Explore and Assess the Data
* Step 3: Define the Data Model
* Step 4: Run ETL to Model the Data
* Step 5: Complete Project Write Up


### Step 1: Scope the Project and Gather Data

#### Scope 
In this project I am using mainly I94 immigration data, which will be integrated with world temperature data and US demographic data. 

#### Describe and Gather Data 
There are 3 datasets
- I94 Immigration Data
    + This data comes from the US National Tourism and Trade Office. This contains information on entry to the united states
- World Temperature Data
    + This dataset comes from Kaggle and includes the temperatures of various cities in the world.
- U.S. City Demographic Data
    + This dataset contains information about the demographics of all US cities and census-designated places with a population greater or equal to 65,000.
    
 ### Step 2: Explore and Assess the Data
 
 Step 3: Define the Data Model
3.1 Conceptual Data Model
The immigration fact table is the central in this star schema. This table's data comes from the immigration data sets.

immigration_fact

record_id: double
year: double
month: double
city_code: string
state_code: string
arrive_date: double
departure_date: double
mode: double
visatype: string
arrival_dm contains the arrival date related data

arrival_dm

arrdate: string
arrival_day: integer
arrival_month: integer
arrival_year: integer
id: long (nullable = false)
df_USTemperature_dim contains average temperature in US cities grouped by month

df_USTemperature_dim

Country: string
City: string
month: long
AverageTemperature: double
demographics_dim contains demographic data of the areas

demographics_dim

City: string
State: string
Median Age: double
Male Population: double
Female Population: double
Total Population: long
State Code: string
3.2 Mapping Out Data Pipelines
Read Data
Drop columns with 90% above missing data and other cleansing
Insert to fact table

Step 4: Run Pipelines to Model the Data¶

