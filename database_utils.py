# Import libraries
from sqlalchemy import create_engine, inspect
import yaml

# Import classes and methods
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

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
        self.df = df

        """Report server and database details"""
        DATABASE_TYPE = "postgresql"
        DBAPI = "psycopg2"
        HOST = "localhost"
        USER = "postgres"
        PASSWORD = "yqcjftVD644"
        DATABASE = "Sales_Data"
        PORT = 5432

        """Store the data in the database"""
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        self.df.to_sql("dim_users", engine, if_exists = "replace")

# Create instances for each class
db_connector = DatabaseConnector()
db_extractor = DataExtractor()
db_cleaner = DataCleaning()

# Retrieve the name of the table that contains user data
user_table = db_connector.list_db_tables()

# Extract and read user data from the database
user_data = db_extractor.read_rds_table(db_connector, "legacy_users")

# Perform the cleaning of user data
df = db_cleaner.clean_user_data(user_data)

# Use the method to upload user data in the database
db_connector.upload_to_db(df)