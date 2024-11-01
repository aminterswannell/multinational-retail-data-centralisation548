from data_extraction import DataExtractor
from database_utils import DatabaseConnector
from data_cleaning import DataCleaning
import pandas as pd
import yaml
import psycopg2

dbc = DatabaseConnector('db_creds.yaml')
print(dbc.read_db_creds())

source_dc = DatabaseConnector('db_creds.yaml')
dest_dc = DatabaseConnector('sales_data_db_creds.yaml')

source_de = DataExtractor('db_creds.yaml')
dest_de = DataExtractor('sales_data_db_creds.yaml')

source_creds = source_dc.read_db_creds()
dest_creds = dest_dc.read_db_creds()

s_host = source_creds['RDS_HOST']
s_username = source_creds['RDS_USER']
s_password = source_creds['RDS_PASSWORD']
s_database = source_creds['RDS_DATABASE']
s_port = source_creds['RDS_PORT']

d_host = dest_creds['RDS_HOST']
d_username = dest_creds['RDS_USER']
d_password = dest_creds['RDS_PASSWORD']
d_database = dest_creds['RDS_DATABASE']
d_port = dest_creds['RDS_PORT']

source_db_uri = f"postgresql+psycopg2://{s_username}:{s_password}@{s_host}:{s_port}/{s_database}"
dest_db_uri = f"postgresql+psycopg2://{d_username}:{d_password}@{d_host}:{d_port}/{d_database}"

source_db_conn = DatabaseConnector(source_db_uri)
dest_db_conn = DatabaseConnector(dest_db_uri)

table_name = source_db_conn.list_db_tables(source_db_uri)[2] 
print(table_name)
user_data_df = source_de.read_rds_table(source_db_conn, table_name)

clean = DataCleaning()
clean_user_data_df = clean.clean_user_data(user_data_df)

engine = dest_db_conn.init_db_engine() 
dest_db_conn.upload_to_db(clean_user_data_df, 'dim_users', engine)
