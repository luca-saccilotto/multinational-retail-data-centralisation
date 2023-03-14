# Import libraries
from sqlalchemy import create_engine, inspect
import yaml

# Create the class and methods
class DatabaseConnector:

    # Create a method that will read the credentials and return a dictionary
    def read_db_creds(self):
        with open("db_creds.yaml", "r") as f:
            credentials = yaml.safe_load(f)
            return credentials
    
    # Create a method that will initialise and return a database engine
    def init_db_engine(self):
        credentials = self.read_db_creds()
        
        """Use the dictionary to set variables"""
        DATABASE_TYPE = "postgresql"
        DBAPI = "psycopg2"
        HOST = credentials["RDS_HOST"]
        USER = credentials["RDS_USER"]
        PASSWORD = credentials["RDS_PASSWORD"]
        DATABASE = credentials["RDS_DATABASE"]
        PORT = credentials["RDS_PORT"]

        """Create a database engine"""
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        
        return engine

    # Create a method to list all the tables in the database
    def list_db_tables(self):
        engine = self.init_db_engine()

        """Retrieve information about the tables inside the database"""
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        
        return table_names
    
    # Create a method to upload the data in the database
    def upload_to_db(self, df):
        credentials = self.read_db_creds()

        """Report server and database details"""
        DATABASE_TYPE = "postgresql"
        DBAPI = "psycopg2"
        HOST = credentials["SQL_HOST"]
        USER = credentials["SQL_USER"]
        PASSWORD = credentials["SQL_PASSWORD"]
        DATABASE = credentials["SQL_DATABASE"]
        PORT = credentials["SQL_PORT"]

        """Store the data in the database"""
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        df.to_sql("dim_date_times", engine, if_exists = "replace")