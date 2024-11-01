import yaml
from sqlalchemy import create_engine, inspect
import psycopg2


class DatabaseConnector():
         
     def __init__(self, creds):
         self.creds = creds

     def read_db_creds(self):
         with open(self.creds, 'r') as stream:
             creds = yaml.safe_load(stream)
         return creds   

     def init_db_engine(self, conn_creds):
         conn_creds = self.read_db_creds()  
         host = conn_creds['RDS_HOST']
         username = conn_creds['RDS_USER']
         password = conn_creds['RDS_PASSWORD']
         database = conn_creds['RDS_DATABASE']
         port = conn_creds['RDS_PORT']
         db_conn_url = f"{'postgresql'}://{username}:{password}@{host}:{port}/{database}"

         engine = create_engine(db_conn_url)
         return engine
     
     def list_db_tables(self, engine):
         db_conn_creds = self.read_db_creds()
         engine = create_engine(db_conn_creds)
         #engine = self.init_db_engine()
         engine.connect()
         inspector = inspect(engine)
         return inspector.get_table_names()
     

     
     def upload_to_db(self, db_creds, df, table_name):
         db_creds = self.read_db_creds()
         local_engine = create_engine(f"postgresql+psycopg2://{db_creds['USER']}:{db_creds['PASSWORD']}@{db_creds['HOST']}:{db_creds['PORT']}/{db_creds['DATABASE']}")
         local_engine.connect()
         df.to_sql(table_name, local_engine, if_exists='replace')


