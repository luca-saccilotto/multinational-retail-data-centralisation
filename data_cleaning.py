# Import libraries
from data_extraction import db_extractor
import pandas as pd

# Create the class and methods
class DataCleaning:

    # Initialize the object's attributes
    def __init__(self, db_extractor, df):
        self.db_extractor = db_extractor
        self.df = df

    # Create a method to standardise the phone number
    def standard_phone_number(self):
        for index, row in self.df.iterrows():
            phone_number = row["phone number"]
            
            """Remove whitespaces and hyphens from the phone number"""
            phone_number = phone_number.replace(" ", "")
            phone_number = phone_number.replace("-", "")

            """Add "00" if the number doesn't start with that"""
            if not phone_number.startswith("00"):
                phone_number = "00" + phone_number
            
            """Remove "+" if it is first character"""
            if phone_number.startswith("+"):
                phone_number = phone_number[1:]
            
            self.df.at[index, "phone number"] = phone_number

        return self.df

    # Create a method to clean the user data
    def clean_user_data(self, df):
        df = self.db_extractor.read_rds_table()

        """Remove null values and duplicates"""
        self.df = self.df.dropna()
        self.df = self.df.drop_duplicates()

        """Remove incorrectly typed values"""
        self.df = self.df[self.df["country_code"].str.contains("GB|DE|US")]
        self.df = self.df[self.df["country"].str.contains("United Kingdom|Germany|United States")]

        """Return standardize phone numbers and dates"""
        self.df = self.standard_phone_number()
        self.df["date_of_birth"] = pd.to_datetime(self.df["date_of_birth"], infer_datetime_format = True, errors = "coerce")
        self.df["join_date"] = pd.to_datetime(self.df["join_date"], infer_datetime_format = True, errors = "coerce")

        return self.df

# Create an instance for the class
db_cleaner = DataCleaning()

# Perform the cleaning of the user data
user_data = db_cleaner.clean_user_data(db_extractor, df)
print(user_data)