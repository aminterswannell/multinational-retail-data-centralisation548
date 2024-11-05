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
         user_df['join_date'] = pd.to_datetime(user_df['join_date'], infer_datetime_format=True, errors='coerce') 
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
