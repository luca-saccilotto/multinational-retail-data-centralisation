# Import libraries
import pandas as pd
import requests
import tabula
import boto3
from botocore import UNSIGNED
from botocore.client import Config

# Create the class and methods
class DataExtractor:

    # Create a method that extracts and reads user data from the database
    def read_rds_table(self, db_connector, table_name):
        engine = db_connector.init_db_engine()
        user_data = pd.read_sql_table(table_name, engine)
        return user_data
    
    # Create a method that extracts and reads card details from a PDF document
    def retrieve_pdf_data(self, link):
        tables = tabula.read_pdf(link, lattice = True, pages = "all")
        card_details = pd.concat(tables)
        return card_details
    
    # Create a method to get the number of stores using an API  
    def list_number_of_stores(self, url, headers):
        response = requests.get(url, headers = headers)

        """Return the number of stores if response status code is successful"""
        if response.status_code == 200:
            data = response.json()
            return data["number_stores"]
        else:
            return None
    
    # Create a method to extract all the stores details from the API as DataFrame
    def retrieve_stores_data(self, store_number, url, headers):
        store_data = []

        for store in range(store_number):
            response = requests.get(url + str(store), headers = headers)

            """Return stores details if response status code is successful"""
            if response.status_code == 200:
                store_data.append(list(response.json().values()))
                column_headings = response.json().keys()
            else:
                return None
            
        store_details = pd.DataFrame(data = store_data, columns = column_headings)

        return store_details
    
    # Create methods to download and extract product information stored in an S3 bucket on AWS
    def extract_from_s3(self, bucket_name, object_name, file_name):
        s3 = boto3.client("s3", config = Config(signature_version = UNSIGNED))
        s3.download_file(bucket_name, object_name, file_name)
        product_details = pd.read_csv(file_name)
        return product_details
    
    def extract_events_data(self, bucket_name, object_name, file_name):
        s3 = boto3.client("s3", config = Config(signature_version = UNSIGNED))
        s3.download_file(bucket_name, object_name, file_name)
        date_events = pd.read_json(file_name)
        return date_events