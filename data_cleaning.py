import pandas as pd
import numpy as np
from data_extraction import DataExtractor as de
from database_utils import DatabaseConnector as dc

creds = dc('db_creds.yaml').read_db_creds()
engine = dc('db_creds.yaml').init_db_engine(creds)

user_df = de('db_creds.yaml').read_rds_table('legacy_users', engine)

class DataCleaning():

     def __init__(self):
         pass

     def clean_user_data(self, user_df):
         user_df['join_date'] = pd.to_datetime(user_df['join_date'], infer_datetime_format=True, errors='coerce') 
         user_df.dropna(subset = ['join_date'], inplace=True)
         print(user_df.head())
    
         return user_df
     
