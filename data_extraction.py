import pandas as pd
import yaml
import tabula
import psycopg2
from sqlalchemy import create_engine
import requests
import json
import boto3

class DataExtractor():
     
     def __init__(self, filename):
         self.filename = filename

     def read_rds_table(self, table_name, engine):
         return pd.read_sql_table(table_name, engine)
    
     def retrieve_pdf_data(self, pdf_link):
         df_pdf = tabula.read_pdf(pdf_link, pages='all', multiple_tables=True)
         return pd.concat(df_pdf, ignore_index=True)
     
     def list_number_of_stores(self, number_store_endpoint, key):
         response = requests.get(number_store_endpoint,headers=key)
         info = response.text
         info_json = json.loads(info)
         number_stores = info_json['number_stores']
         return number_stores
    
     def retrieve_stores_data(self,retrieve_store_endpoint, number_stores, key):
         store_data = []
         for i in range(number_stores):
             response = requests.get(f"{retrieve_store_endpoint}{i}", headers=key)
             info = response.text
             info_json = json.loads(info)
             store_data.append(info_json)

         stores_df = pd.DataFrame(store_data)
         return stores_df
     
     def extract_from_s3(self, s3_address):
         s3 = boto3.client('s3')
         s3_bucket = 'data-handling-public'
         object = 'products.csv'
         file = 'products.csv'
         s3.download_file(s3_bucket,object,file)
         products_df = pd.read_csv('./products.csv')
         return products_df 