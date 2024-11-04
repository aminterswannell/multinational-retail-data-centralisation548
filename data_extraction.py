import pandas as pd
import yaml
import tabula
import psycopg2
from sqlalchemy import create_engine

class DataExtractor():
     
     def __init__(self, filename):
        self.filename = filename

     def read_rds_table(self, table_name, engine):
         return pd.read_sql_table(table_name, engine)
    
     def retrieve_pdf_data(self, pdf_link):
         df_pdf = tabula.read_pdf(pdf_link, pages='all', multiple_tables=True)
         df_card_details = pd.concat(df_pdf, ignore_index=True)
         return df_card_details
     
