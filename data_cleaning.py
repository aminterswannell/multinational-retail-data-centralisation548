import pandas as pd
import numpy as np
from data_extraction import DataExtractor as de
from database_utils import DatabaseConnector as dc
import tabula

creds = dc('db_creds.yaml').read_db_creds()
engine = dc('db_creds.yaml').init_db_engine(creds)

user_df = de('db_creds.yaml').read_rds_table('legacy_users', engine)
card_df = de('db_creds.yaml').retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')


class DataCleaning():

     def __init__(self):
         pass

     def clean_user_data(self, user_df):
         user_df['join_date'] = pd.to_datetime(user_df['join_date'], errors='coerce') 
         user_df.dropna(subset = ['join_date'], inplace=True)
         print(user_df.head())
    
         return user_df
     
     def clean_card_data(self, card_df):
         
         card_df.replace('NULL',np.nan,inplace=True)
         card_df.dropna(subset=['card_number'],how='any',axis=0,inplace=True)
         card_df['card_number'] = card_df['card_number'].apply(str)
         card_df = card_df[~card_df['card_number'].str.contains('[a-zA-Z?]',na=False)]

         clean_card_df = pd.DataFrame(card_df)

         return clean_card_df

     def clean_store_data(self, store_data):
         
         store_data.replace({'continent': ['eeEurope', 'eeAmerica']}, {'continent': ['Europe', 'America']}, inplace=True)
         store_data.replace('NULL',np.nan,inplace=True)
         store_data.drop(store_data.columns[0], axis=1,inplace=True)
         store_data.drop(columns='lat',inplace=True)
         store_data['opening_date'] = pd.to_datetime(store_data['opening_date'],errors='coerce')
         store_data['staff_numbers'] = pd.to_numeric(store_data['staff_numbers'],errors='coerce')
         store_data.dropna(subset=['staff_numbers'],axis=0,inplace=True)
 
         return store_data
     
     def convert_product_weights(self,product_weight):
        
         if 'kg' in product_weight:
             product_weight = product_weight.replace('kg','')
             product_weight = float(product_weight)
         elif 'ml' in product_weight:
             product_weight = product_weight.replace('ml','')
             product_weight = float(product_weight) / 1000
         elif 'g' in product_weight:
             product_weight = product_weight.replace('g','')
             product_weight = float(product_weight) / 1000
         elif 'oz' in product_weight:
             product_weight = product_weight.replace('oz','')
             product_weight = float(product_weight) * 0.0283495
        
         return product_weight
     
     def  clean_products_data(self, products_df):
         products_df=self.convert_product_weights(products_df)
         products_df.dropna(subset=['uuid', 'product_code'], inplace=True)
         products_df['date_added']=pd.to_datetime(products_df['date_added'], format='%Y-%m-%d', errors='coerce')
        
         return products_df
         
     def clean_orders_data(self, orders_table):
         
         orders_table.drop(columns='first_name',axis=1,inplace=True)
         orders_table.drop(columns='last_name',axis=1,inplace=True)
         orders_table.drop(columns='1',axis=1,inplace=True)
         orders_table.drop(columns='level_0',axis=1,inplace=True)
         orders_table.drop(orders_table.columns[0],axis=1,inplace=True)
          
         return orders_table 
     
     def clean_date_times(self, date_details_df):
        date_details_df['day'] = pd.to_numeric(date_details_df['day'], errors='coerce')
        date_details_df.dropna(subset=['day', 'year', 'month'], inplace=True)
        date_details_df['timestamp'] = pd.to_datetime(date_details_df['timestamp'], format='%H:%M:%S', errors='coerce')

        return date_details_df


