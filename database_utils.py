import yaml
from psycopg2 import connect
from sqlalchemy import create_engine, inspect



class DatabaseConnector():
     """
     Class to connect to relational database service.
     """
         
     def __init__(self, creds):
         """
         Initializes the DatabaseConnector class.

         Args:
             creds (str): The credentials for the RDS.
         """
         self.creds = creds

     def read_db_creds(self):
         """
         Method to read RDS credentials from .yaml file.

         Returns:
             str : RDS credentials loaded from .yaml file.
         """
         with open(self.creds, 'r') as stream:
             loaded_creds = yaml.safe_load(stream)
         return loaded_creds   

     def init_db_engine(self, connection_creds):
         """
         Method to initiate database engine.

         Args:
             connection_creds (str): RDS credentials obtained from using read_db_creds method.

         Returns:
             engine: The database engine.
         """
         connection_creds = self.read_db_creds()
         host = connection_creds['RDS_HOST']
         username = connection_creds['RDS_USER']
         password = connection_creds['RDS_PASSWORD']
         database = connection_creds['RDS_DATABASE']
         port = connection_creds['RDS_PORT']
         db_connection_url = f"{'postgresql'}://{username}:{password}@{host}:{port}/{database}"

         engine = create_engine(db_connection_url)
         return engine
     
     def list_db_tables(self, engine):
         """
         Method to list the names of RDS tables.

         Args:
             engine: The database engine.

         Returns:
             list: List of the database table names.
         """
         engine.connect()
         inspector = inspect(engine)
         return inspector.get_table_names()
     
     def upload_to_db(self, db_creds, df, table_name):
         """
         Method to upload the data to a RDS.

         Args:
             db_creds (str): Database credentials.
             df (pd.DataFrame): DataFrame containing data to be uploaded to database.
             table_name (str): Table name to be uploaded to database.
         """
         db_creds = self.read_db_creds()
         local_engine = create_engine(f"postgresql+psycopg2://{db_creds['RDS_USER']}:{db_creds['RDS_PASSWORD']}@{db_creds['RDS_HOST']}:{db_creds['RDS_PORT']}/{db_creds['RDS_DATABASE']}")
         local_engine.connect()
         df.to_sql(table_name, local_engine, if_exists='replace')


