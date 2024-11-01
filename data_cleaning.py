import pandas as pd
import numpy as np
from data_extraction import DataExtractor as de

class DataCleaning():

     def __init__(self):
         pass

     def clean_user_data(self, df):
         df = de('db_creds.yaml').read_rds_table('legacy_users')
         df['date_of_birth'] = pd.to_datetime(df['date_of_birth'],  infer_datetime_format=True, errors='coerce')
         df['join_date'] = pd.to_datetime(df['join_date'], infer_datetime_format=True, errors='coerce')
         df.dropna(subset=['date_of_birth','join_date'], inplace=True)
        
         return df
     
