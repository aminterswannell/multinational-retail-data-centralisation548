import boto3
import json
import pandas as pd
import psycopg2
import requests
import tabula
import yaml

from sqlalchemy import create_engine

class DataExtractor():
     """
     Class used to extract data from a variety of sources.
     """
     
     def __init__(self, filename):
         """
         Initializes the DataExtractor class.

         Args:
             filename (str): The unique path to the .yaml file that stores the database credentials.  
         """
         self.filename = filename
        
     def read_rds_table(self, table_name, engine):
         """
         Method to read data from an RDS table.

         Args:
             table_name (str): The name of the desired table from the RDS.
             engine: A DatabaseConnector object.

         Returns:
             pd.DataFrame: The data from the RDS table.
         """
         return pd.read_sql_table(table_name, engine)
    
     def retrieve_pdf_data(self, pdf_link):
         """
         Retrieves data stored in a pdf file.

         Args:
             pdf_link (str): Link to pdf document.

         Returns:
             pd.DataFrame: The data from the pdf file.
         """
         df_pdf = tabula.read_pdf(pdf_link, pages='all', multiple_tables=True)
         return pd.concat(df_pdf, ignore_index=True)
     
     def list_number_of_stores(self, number_store_endpoint, key):
         """
         Lists the number of stores.

         Args:
             number_store_endpoint (str): The endpoint location for the number of stores.
             key (str): API key.

         Returns:
             int: The number of stores.
         """
         response = requests.get(number_store_endpoint,headers=key)
         info = response.text
         info_json = json.loads(info)
         number_stores = info_json['number_stores']
         return number_stores
    
     def retrieve_stores_data(self, retrieve_store_endpoint, number_stores, key):
         """
         _summary_

         Args:
             retrieve_store_endpoint (str): Endpoint location for the stores data.
             number_stores (int): Number of stores.
             key (str): API key.

         Returns:
             pd.DataFrame: All stores data.
         """
         store_data = []
         for i in range(number_stores):
             response = requests.get(f"{retrieve_store_endpoint}{i}", headers=key)
             info = response.text
             info_json = json.loads(info)
             store_data.append(info_json)

         stores_df = pd.DataFrame(store_data)
         return stores_df
     
     def extract_from_s3(self, s3_address):
         """
         Extracts data from s3 bucket.

         Args:
             s3_address (str): The s3 bucket address.

         Returns:
             pd.DataFrame: The extracted data from the s3 bucket.
         """
         s3 = boto3.client('s3')
         s3_bucket = 'data-handling-public'
         object = 'products.csv'
         file = 'products.csv'
         s3.download_file(s3_bucket,object,file)
         products_df = pd.read_csv('./products.csv')
         return products_df 
     
     def extract_from_s3_json(self, s3_link):
         """
         Extract data from an s3 bucket using a JSON file link.

         Args:
             s3_link (str): Link to JSON file stored on s3.

         Returns:
             pd.DataFrame: The extracted data from the JSON file.
         """
         s3 = boto3.client('s3')
         s3_bucket = 'data-handling-public'
         object = 'date_details.json'
         file = 'date_details.json'
         s3.download_file(s3_bucket,object,file)
         date_details_df = pd.read_json('./date_details.json')
         return date_details_df 