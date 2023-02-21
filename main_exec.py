#%%

# Import classes and methods
from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

# Create instances for each class
db_connector = DatabaseConnector()
data_extractor = DataExtractor()
data_cleaning = DataCleaning()

#%%

## Retrieve the name of the table that contains user data
user_table = db_connector.list_db_tables()

## Extract and read user data from the database
user_data = data_extractor.read_rds_table(db_connector, "legacy_users")

## Perform the cleaning of user data
user_data = data_cleaning.clean_user_data(user_data)

## Use the method to upload user data in the database
db_connector.upload_to_db(user_data)

#%%

## Extract and read card details from a PDF document
card_details = data_extractor.retrieve_pdf_data(
    link = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf")

## Perform the cleaning of card data
card_details = data_cleaning.clean_card_data(card_details)

## Use the method to upload card details in the database
db_connector.upload_to_db(card_details)

#%%

## Extract the number of stores using an API
store_number = data_extractor.list_number_of_stores(
    url = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores",
    headers = {"x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"})

## Extract all the store details from the API as DataFrame
store_details = data_extractor.retrieve_stores_data(
    store_number, 
    url = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/", 
    headers = {"x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"})

## Perform the cleaning of store data
store_details = data_cleaning.clean_store_data(store_details)

## Use the method to upload store details in the database
db_connector.upload_to_db(store_details)

#%%

## Extract product information stored in an S3 bucket on AWS
product_details = data_extractor.extract_from_s3(
    bucket_name = "data-handling-public",
    object_name = "products.csv",
    file_name = "products.csv")

## 
