import numpy as np
import pandas as pd
from data_extraction import DataExtractor as de
from database_utils import DatabaseConnector as dc
import tabula
import re 

creds = dc('db_creds.yaml').read_db_creds()
engine = dc('db_creds.yaml').init_db_engine(creds)

user_df = de('db_creds.yaml').read_rds_table('legacy_users', engine)
card_df = de('db_creds.yaml').retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')


class DataCleaning():
     """
     Class used to clean data extracted from a variety of sources.
     """

     def __init__(self):
         """
         Initializes the DataCleaning class.
         """
         pass

     def clean_user_data(self, user_df):
         """
         Cleans user data by removing rows with missing values and date errors.

         Args:
             user_df (pd.DataFrame): DataFrame containing users data.

         Returns:
             pd.DataFrame: The clean user data.
         """
         user_df['join_date'] = pd.to_datetime(user_df['join_date'], errors='coerce') 
         user_df.dropna(subset = ['join_date'], inplace=True)
    
         return user_df
     
     def clean_card_data(self, card_df):
         """
         Cleans card data by replacing or dropping null values and correcting errors with formatting.

         Args:
             card_df (pd.DataFrame): DataFrame containing card data.

         Returns:
             pd.DataFrame: The clean card data.
         """
         
         card_df.replace('NULL',np.nan,inplace=True)
         card_df.dropna(subset=['card_number'],how='any',axis=0,inplace=True)
         card_df['card_number'] = card_df['card_number'].apply(str)
         card_df = card_df[~card_df['card_number'].str.contains('[a-zA-Z?]',na=False)]

         clean_card_df = pd.DataFrame(card_df)

         return clean_card_df

     def clean_store_data(self, store_data):
         """
         Cleans store data by correcting formatting of values and dates.

         Args:
             store_data (pd.DataFrame): DataFrame containing store data.

         Returns:
             pd.DataFrame: The clean store data.
         """
         
         store_data.replace({'continent': ['eeEurope', 'eeAmerica']}, {'continent': ['Europe', 'America']}, inplace=True)
         store_data.replace('NULL',np.nan,inplace=True)
         store_data.drop(store_data.columns[0], axis=1,inplace=True)
         store_data.drop(columns='lat',inplace=True)
         store_data['opening_date'] = pd.to_datetime(store_data['opening_date'],errors='coerce')
         store_data['staff_numbers'] = pd.to_numeric(store_data['staff_numbers'],errors='coerce')
         store_data.dropna(subset=['staff_numbers'],axis=0,inplace=True)
 
         return store_data
     
     def convert_product_weights(self, products_df):
        """
        Convert product weights to kilograms.

        Args:
        - products_df (pd.DataFrame): The DataFrame containing product data.

        Returns:
        - pd.DataFrame: The DataFrame with weights converted to kilograms.
        """
        def convert_to_kg(weight_str):
            try:
                if isinstance(weight_str, str):
                    value, unit = re.match(r'(\d+\.?\d*)\s*([a-zA-Z]+)', weight_str).groups()
                    if unit.lower() == 'g':
                        return float(value) / 1000
                    elif unit.lower() == 'ml':
                        return float(value) / 1000
                    else:
                        return float(value)
            except (AttributeError, ValueError):
                return None
        products_df['weight_kg'] = products_df['weight'].apply(convert_to_kg)
        return products_df
     
     def  clean_products_data(self, products_df):
         """
         Cleans product data 

         Args:
             products_df (pd.DataFrame): DataFrame containing products information.

         Returns:
             pd.DataFrame: Clean products data.
         """
         products_df=self.convert_product_weights(products_df)
         products_df.dropna(subset=['uuid', 'product_code'], inplace=True)
         products_df['date_added']=pd.to_datetime(products_df['date_added'], format='%Y-%m-%d', errors='coerce')
        
         return products_df
         
     def clean_orders_data(self, orders_table):
         """
         Cleans orders data by dropping columns.

         Args:
             orders_table (pd.DataFrame): DataFrame containing orders data.

         Returns:
             pd.DataFrame: Clean orders data.
         """
         
         orders_table.drop(columns='first_name',axis=1,inplace=True)
         orders_table.drop(columns='last_name',axis=1,inplace=True)
         orders_table.drop(columns='1',axis=1,inplace=True)
         orders_table.drop(columns='level_0',axis=1,inplace=True)
         orders_table.drop(orders_table.columns[0],axis=1,inplace=True)
          
         return orders_table 
     
     def clean_date_times(self, date_details_df):
         """
         Cleans dates and times using pandas methods.

         Args:
             date_details_df (pd.DataFrame): DataFrame containing date details.

         Returns:
             pd.DataFrame: Clean date details.
         """

         date_details_df['day'] = pd.to_numeric(date_details_df['day'], errors='coerce')
         date_details_df.dropna(subset=['day', 'year', 'month'], inplace=True)
         date_details_df['timestamp'] = pd.to_datetime(date_details_df['timestamp'], format='%H:%M:%S', errors='coerce')

         return date_details_df


