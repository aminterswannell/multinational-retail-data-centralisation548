from data_extraction import DataExtractor as de
from database_utils import DatabaseConnector as dc
from data_cleaning import DataCleaning as dcl
import pandas as pd
import yaml
import psycopg2

source_connector = dc('db_creds.yaml')
destination_connector = dc('sales_data_db_creds.yaml')

source_creds = source_connector.read_db_creds()
destination_creds = destination_connector.read_db_creds()

source_host = source_creds['RDS_HOST']
source_username = source_creds['RDS_USER']
source_password = source_creds['RDS_PASSWORD']
source_database = source_creds['RDS_DATABASE']
source_port = source_creds['RDS_PORT']

destination_host = destination_creds['RDS_HOST']
destination_username = destination_creds['RDS_USER']
destination_password = destination_creds['RDS_PASSWORD']
destination_database = destination_creds['RDS_DATABASE']
destination_port = destination_creds['RDS_PORT']

source_db_uri = f"postgresql+psycopg2://{source_username}:{source_password}@{source_host}:{source_port}/{source_database}"
destination_db_uri = f"postgresql+psycopg2://{destination_username}:{destination_password}@{destination_host}:{destination_port}/{destination_database}"

print(source_db_uri)

source_db_connection = source_connector.init_db_engine(source_db_uri)
destination_db_connection = destination_connector.init_db_engine(destination_db_uri)

source_extractor = de('db_creds.yaml')
desination_extractor = de('sales_data_db_creds.yaml')

table_name = source_connector.list_db_tables(source_db_connection)[2] 
print(table_name)
user_data_df = source_extractor.read_rds_table(table_name, engine=source_db_connection)

clean = dcl()
clean_user_data_df = clean.clean_user_data(user_data_df)

creds = destination_db_uri

destination_connector.upload_to_db(creds, clean_user_data_df, 'dim_users')

pdf_link = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'

card_data = source_extractor.retrieve_pdf_data(pdf_link)

clean_card_data_df = clean.clean_card_data(card_data)

destination_connector.upload_to_db(creds, clean_card_data_df, 'dim_card_details')

number_store_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
retrieve_store_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/'
api_key = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}

number_stores = source_extractor.list_number_of_stores(number_store_endpoint, api_key)

store_data = source_extractor.retrieve_stores_data(retrieve_store_endpoint, number_stores, api_key)

clean_store_data = clean.clean_store_data(store_data)

destination_connector.upload_to_db(creds, clean_store_data, 'dim_store_details')

s3_address = 's3://data-handling-public/products.csv'

products_df = source_extractor.extract_from_s3(s3_address)

clean_products_df = clean.convert_product_weights(products_df)

clean_products_df = clean.clean_products_data(clean_products_df)

destination_connector.upload_to_db(creds, clean_products_df, 'dim_products')

table_names_list = source_connector.list_db_tables(source_db_connection)
print(table_names_list)

orders_table_name = source_connector.list_db_tables(source_db_connection)[3]
print(orders_table_name)
