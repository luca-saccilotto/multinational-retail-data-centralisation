# Import libraries
import pandas as pd
import re

# Create the class and methods
class DataCleaning:

    # Create a method to standardise the phone number
    def standard_phone_number(self, df):
        country_codes = {"GB": "+44", "DE": "+49", "US": "+1"}

        for index, row in df.iterrows():
            phone_number = row["phone_number"]
            country_code = row["country_code"]
            
            """Remove any character that is not a digit"""
            phone_number = re.sub(r"[^\d+]", "", phone_number)

            """Add the prefix if it is not present"""
            if not phone_number.startswith(country_codes[country_code]):
                phone_number = country_codes[country_code] + phone_number

            df.at[index, "phone_number"] = phone_number

        return df

    # Create a method to clean user data
    def clean_user_data(self, df):

        """Remove null values and duplicates"""
        df = df.dropna()
        df = df.drop_duplicates()

        """Replace and remove incorrectly typed values"""
        df = df[df["country"].str.contains("United Kingdom|Germany|United States")]
        df["country_code"] = df["country_code"].replace("GGB", "GB")
        df = df[df["country_code"].str.contains("GB|DE|US")]

        """Return standardize phone numbers and dates"""
        df = self.standard_phone_number(df)
        df["date_of_birth"] = pd.to_datetime(df["date_of_birth"], infer_datetime_format = True, errors = "coerce")
        df["join_date"] = pd.to_datetime(df["join_date"], infer_datetime_format = True, errors = "coerce")

        return df
    
    # Create a method to clean card details
    def clean_card_data(self, df):

        """Remove null values and duplicates"""
        df = df.dropna()
        df = df.drop_duplicates()

        """Remove incorrectly typed values"""
        df = df[df["card_provider"].str.contains("VISA 16 digit|JCB 16 digit|VISA 13 digit|JCB 15 digit|VISA 19 digit|Diners Club / Carte Blanche|American Express|Maestro|Discover|Mastercard")]

        """Return standardize payment dates"""
        df["date_payment_confirmed"] = pd.to_datetime(df["date_payment_confirmed"], infer_datetime_format = True, errors = "coerce")

        """Drop original index and reset numeration"""
        df = df.reset_index(drop = True)

        return df
    
    # Create a method to clean store details
    def clean_store_data(self, df):

        """Remove null values and duplicates"""
        df = df.drop("lat", axis = 1)
        df = df.dropna()
        df = df.drop_duplicates()

        """Remove and replace incorrectly typed values"""
        df = df[~ df.locality.str.contains(r"\d")]
        df = df[pd.to_numeric(df["latitude"], errors = "coerce").notnull()]
        df = df[pd.to_numeric(df["staff_numbers"], errors = "coerce").notnull()]
        df["continent"] = df["continent"].replace({"eeEurope": "Europe", "eeAmerica": "America"})

        """Return standardize opening dates"""
        df["opening_date"] = pd.to_datetime(df["opening_date"], infer_datetime_format = True, errors = "coerce")
        
        """Drop original index and reset numeration"""
        df = df.reset_index(drop = True)

        return df
    
    # Create a method to convert products weight
    def convert_product_weights(self, df):

        """Create an empty column for unit"""
        df["unit"] = pd.NA

        """Loop through the rows of the dataframe"""
        for index, row in df.iterrows():
            weight = str(row["weight"])

            """Check the measure of weight"""
            if "kg" in weight:
                unit = "kg"
            elif "g" in weight:
                unit = "g"
            elif "ml" in weight:
                unit = "ml"
            elif "oz" in weight:
                unit = "oz"
            else:
                continue

            """Save the unit and weight to their respective columns"""
            df.at[index, "unit"] = unit
            df.at[index, "weight"] = weight.replace(unit, "")

            """Take a value that may contain a quantity multiplier and evaluate it"""
            if "x" in weight:
                weight = eval(weight.replace("x", "*").replace(" ", "").replace("g", ""))
            else:
                continue

        """Replace weight of row 1779 with 77"""
        df.at[1779, "weight"] = 77

        """Remove incorrectly typed values"""
        df = df[pd.to_numeric(df["weight"], errors = "coerce").notnull()]

        """Standardize weight type to numeric"""
        df["weight"] = df["weight"].astype(float)

        """Standardize units measure"""
        df.loc[df["unit"] == "g", "weight"] /= 1000
        df.loc[df["unit"] == "ml", "weight"] /= 1000
        df.loc[df["unit"] == "oz", "weight"] /= 35.274

        return df
    
    # Create a method to clean products details
    def clean_product_data(self, df):
        
        """Remove null values and duplicates"""
        df = df.dropna()
        df = df.drop_duplicates()

        """Drop the first and last column"""
        df = df.drop(df.columns[0], axis = 1)
        df = df.drop(columns = ["unit"])

        """Add an index column and rename it"""
        df = df.reset_index().rename(columns = {"index": "id"})

        """Replace values in column"""
        df["removed"] = df["removed"].replace("Still_avaliable", "Available")

        """Return standardize opening dates"""
        df["date_added"] = pd.to_datetime(df["date_added"], infer_datetime_format = True, errors = "coerce")

        return df
    
    # Create a method to clean orders table
    def clean_orders_data(self, df):
        column_names = ["first_name", "last_name", "1", "level_0", "index"]
        df = df.drop(columns = column_names)
        return df
    
    # Create a method to clean date events data
    def clean_events_data(self, df):

        """Remove null values and duplicates"""
        df = df.dropna()
        df = df.drop_duplicates()

        """Remove incorrectly typed values"""
        df = df[df["time_period"].str.contains("Midday|Late_Hours|Evening|Morning")]
        
        return df