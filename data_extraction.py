import pandas as pd
import yaml
import tabula
import psycopg2
from sqlalchemy import create_engine
import requests

class DataExtractor():
     
     def __init__(self, filename):
         self.filename = filename

     def read_rds_table(self, table_name, engine):
         return pd.read_sql_table(table_name, engine)
    
     def retrieve_pdf_data(self, pdf_link):
         df_pdf = tabula.read_pdf(pdf_link, pages='all', multiple_tables=True)
         return pd.concat(df_pdf, ignore_index=True)
     
     def list_number_of_stores(self, header_details, number_stores_endpoint):
         header_details = {'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
         number_stores_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
         stores_list = requests.get(number_stores_endpoint, headers=header_details)
         number_stores = stores_list.json()
         return number_stores

     def retrieve_stores_data(self):
         number_stores = self.list_number_of_stores()
         header_details = {'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
         store_details_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/'
         stores_list = []
         for store_number in range(0, number_stores):
             stores_list.append(requests.get(store_details_endpoint+str(store_number), headers=header_details).json())
         return pd.json_normalize(stores_list)