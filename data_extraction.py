# Import libraries
from database_utils import db_connector
import pandas as pd

# Create the class and methods
class DataExtractor:

    # Create a method that will read the data from the database
    def read_rds_table(self, db_connector, table_name):

        """Assign arguments to instance variables"""
        self.db_connector = db_connector
        self.table_name = table_name

        """Read data from a database and store it as a dataframe"""
        engine = self.db_connector.init_db_engine()
        table = pd.read_sql_table(table_name, engine)
        df = pd.DataFrame(table)

        return df

# Create an instance for the class
db_extractor = DataExtractor()

# Extract user data
user_data = db_extractor.read_rds_table(db_connector, "legacy_users")
print(user_data)