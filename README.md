# Multi-national Retail Data Centralisation Project

## Contents:
- Project Description
- Installation Instructions
- Usage Instructions
- File Structure
- License Information

## Project Description
### Task:
You work for a multinational company that sells various goods across the globe.
Currently, their sales data is spread across many different data sources making it not easily accessible or analysable by current members of the team.
In an effort to become more data-driven, your organisation would like to make its sales data accessible from one centralised location.
Your first goal will be to produce a system that stores the current company data in a database so that it's accessed from one centralised location and acts as a single source of truth for sales data.
You will then query the database to get up-to-date metrics for the business.

### Solution:
By extracting and cleaning the data from the variety of sources so that it was in a more uniform format, it was possible to then centralise this data by uploading it to a local database where they could be queried in SQL.
This was achieved through the creation of three Python classes to perform the necessary extraction, manipulation and uploading of the data, these were utilised through importing to a main document and calling where necessary.
### What I learned:

## Installation Instructions
1. Clone the repository 
2. Installed required packages

## Usage Instructions
1. Extraction, cleaning and uploading data
   - Data needs to be extracted from various sources, two different AWS RDS', two separate AWS S3 buckets, a .pdf and a .csv.
   - This data is to be cleaned and then uploaded to an empty SQL database called sales_data.
   - The required classes are defined in database_utils.py, data_cleaning.py and data_extraction.py, and these are imported and used in main.py.
2. Creating database schema
   - Now the clean data has been uploaded, it is needed to be formatted further to create a star-based schema.
   - This involves various table alterations of the separate tables and the creation of primary and foreign keys for each table that are needed to complete the centralisation of the data.
3. Querying the data
   - The company wants up-to-date metrics for the business so its needed to run a number of queries to find the desired information.

## File Structure
README - Project documentation
LICENSE - MIT

mnrdc:
- database_utils.py contains the DatabaseConnector class for connecting to the relational database service and uploading to the local database.
- data_extraction.py contains the DataExtractor class for extracting data from a variety of data sources.
- data_cleaning.py contains the DataCleaning class for cleaning the extracted data from the different sources.
- main.py contains code run to utilise the imported classes listed above to extract, clean and upload all the necessary data to a centralised database.

database_schema:
- 1_orders_table.sql 
- 2_dim_users.sql
- 3_dim_store_details.sql
- 4_dim_products.sql
- 5_dim_date_times.sql
- 6_dim_card_details.sql
- 7_primary_keys.sql
- 8_foreign_keys.sql

querying_the_data:
- task_1.sql
- task_2.sql
- task_3.sql
- task_4.sql
- task_5.sql
- task_6.sql
- task_7.sql
- task_8.sql
- task_9.sql

## License Information
An MIT License was used for this project.
