import pandas as pd
import yaml
import tabula
from database_utils import DatabaseConnector 

class DataExtractor():
     
     def __init__(self, filename):
        self.filename = filename
        self.db = DatabaseConnector(filename)
        self.rds_db = self.db.init_db_engine(filename)

     def read_rds_table(self, table_name):
         return pd.read_sql_table(table_name, self.rds_db)
    
     def retrieve_pdf_data(self, pdf_link):
         df_pdf = tabula.read_pdf(pdf_link, pages='all', multiple_tables=True)
         df_card_details = pd.concat(df_pdf, ignore_index=True)
         return df_card_details