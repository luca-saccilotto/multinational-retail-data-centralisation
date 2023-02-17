# Import libraries
from sqlalchemy import create_engine
import yaml

class DatabaseConnector:

    # Create a method that will read the credentials and return a dictionary
    def read_db_creds(self):
        with open("../db_creds.yaml", "r") as f:
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
        
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        return engine