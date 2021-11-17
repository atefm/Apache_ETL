# Building an ETL pipeline with Apache Airflow
The goal of the project is to build a dashboard that showcases sales funnel through standard Data Engineering practices and using technologies such as Apache Airflow.

## Data Source
4 CSV files containing structured data. The data files are stored in the 'data' folder
## Overall Solution

- The proposed solution is to build a data pipeline using Apache Airflow as required. The overall strategy is to create two databases namely, **transactional_db** and **data_warehouse_db**. The reason for creating two databases is to avoid using the main database (**transactional_db**) when performing data analysis related tasks. 
- The data stored in the **data_warehouse_db** is to be used to perform transformations and building of dashboard reports.
- The data warehouse is to be updated incrementally.
- Reporting tools such as PowerBI can be used to extract and visualise reports.The tool also allows the reports to be automatically refreshed with new data coming in at predefined intervals. 

## Tasks Completed:
- Creating two databases as mentioned above and the relevant tables associated with them. 
- Populating the tables using the data provided.
- Transforming the data required for sales funnel reporting to avoid expensive **join** operations.


## TODO:
Given the personal time constraints, this project was timeboxed. As the allocated timeline was exhausted, the following tasks still need to be completed:

- Dashboard showcasing sales funnel for each offer and for the data in aggregate. The data required to build this report is pre-computed and stored in the **sales_funnel** table.
- Incremental update of the data in the **data_warehouse_db**
- Calculation of Euro value for non-euro currencies based on either the latest exchange rate or the exchange rate at the time of the deal.

## USAGE
The solution is dockerized and both the data and environmental variable file are providedin this repo for the sake of simplicity. Makefile is provided to auto configure the containers.

When running it for the first time, please run **make build**.

To stop the containers, run **make stop**.

To spin up the containers normally, run **docker-compose up** 



