# Import libraries
import pandas as pd
import re

# Create the class and methods
class DataCleaning:

    # Create a method to standardise the phone number
    def standard_phone_number(self):
        country_codes = {"GB": "+44", "DE": "+49", "US": "+1"}

        for index, row in self.df.iterrows():
            phone_number = row["phone_number"]
            country_code = row["country_code"]
            
            """Remove any character that is not a digit"""
            phone_number = re.sub(r"[^\d+]", "", phone_number)

            """Add the prefix if it is not present"""
            if not phone_number.startswith(country_codes[country_code]):
                phone_number = country_codes[country_code] + phone_number

            self.df.at[index, "phone_number"] = phone_number

        return self.df

    # Create a method to clean user data
    def clean_user_data(self, df):
        self.df = df

        """Remove null values and duplicates"""
        self.df = self.df.dropna()
        self.df = self.df.drop_duplicates()

        """Replace and remove incorrectly typed values"""
        self.df = self.df[self.df["country"].str.contains("United Kingdom|Germany|United States")]
        self.df["country_code"] = self.df["country_code"].replace("GGB", "GB")
        self.df = self.df[self.df["country_code"].str.contains("GB|DE|US")]

        """Return standardize phone numbers and dates"""
        self.df = self.standard_phone_number()
        self.df["date_of_birth"] = pd.to_datetime(self.df["date_of_birth"], infer_datetime_format = True, errors = "coerce")
        self.df["join_date"] = pd.to_datetime(self.df["join_date"], infer_datetime_format = True, errors = "coerce")

        return self.df
    
    # Create a method to clean card data
    def clean_card_data(self, df):
        self.df = df

        """Remove null values and duplicates"""
        self.df = self.df.dropna()
        self.df = self.df.drop_duplicates()

        """Remove incorrectly typed values"""
        self.df = self.df[self.df["card_provider"].str.contains("VISA 16 digit|JCB 16 digit|VISA 13 digit|JCB 15 digit|VISA 19 digit|Diners Club / Carte Blanche|American Express|Maestro|Discover|Mastercard")]

        """Return standardize payment dates"""
        self.df["date_payment_confirmed"] = pd.to_datetime(self.df["date_payment_confirmed"], infer_datetime_format = True, errors = "coerce")

        """Drop original index and reset numeration"""
        self.df = self.df.reset_index(drop = True)

        return self.df