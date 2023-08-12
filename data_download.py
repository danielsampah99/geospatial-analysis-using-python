# data download.py

# Importing necessary modules.
from sentinelsat import (SentinelAPI, geojson_to_wkt, read_geojson)
from datetime import date
import geopandas
import os


class DownloadData():
    def __init__(self, *args, **kwargs):
        self.username = "niiniinii"
        self.password = "Bab0@satellite"
        self.api_url = "https://apihub.copernicus.eu/apihub"
        
        self.connect_to_api()
        self.convert_geojson_file()
        self.search_parameters()
        self.create_products_csv_file()
        self.download_all_products()
        
    def connect_to_api(self):
        """Creating a connection to the sentinehub API."""
        print("Connecting to copernicus.eu...")
        self.api = SentinelAPI(user=self.username, 
                    password=self.password, 
                    api_url=self.api_url, 
                    show_progressbars=True, 
                    timeout=300)
        print("Successfully connected copernicus.eu\n\n\n")
        
    def convert_geojson_file(self):
        """Convert the geojson file to a well-known text format."""
        # Path of the geojson file. 
        self.geojson_file_object = r"C:\Users\danny\OneDrive\Documents\Sentinel Data\ghana.geojson"

        # Loading the geojson file.
        self.geojson_file_raw = read_geojson(geojson_file=self.geojson_file_object)

        # Convert the geojson file to a well-known text file.
        self.footprint = geojson_to_wkt(geojson_obj=self.geojson_file_raw, 
                       decimals=4)
    
    def search_parameters(self):
        """Creating parameters of the search query"""
        print(f"Beginning query of products.")

        # Start time of the query.
        start_input = input("Enter the start date of your query in the format of year month day (2022 1 1) separated by space: ")
        start_year, start_month, start_day = map(int, start_input.split())
        self.start_time = date(year=start_year, month=start_month, day=start_day)

        # End Time of query - Requesting and processing input from the user.
        end_input = input("Enter the end date of your query in the format of year month day (2022 12 31) separated by space: ")
        end_year, end_month, end_day = map(int, end_input.split())
        self.end_time = date(year=end_year, month=end_month, day=end_day)

        # Cloud cover percentage.
        cloud_cover = input("Enter the miinimum and maximum cloud cover values separated by space. \n\t Example: 0 10 for products with a cloud cover range of 0 and 10.: ")
        min_cloud, max_cloud = map(int, cloud_cover.split())

        "The options for area relation include {'Intersects', 'Contains', 'IsWithin'} and are all case sensitive."

        self.products = self.api.query(area=self.footprint, 
                                       date=(self.start_time, self.end_time), 
                                       area_relation="IsWithin", 
                                       cloudcoverpercentage=(min_cloud, max_cloud), 
                                       platformname="Sentinel-2", 
                                    #    producttype="S2MSI2A"
                                    )
        
        # Create a list of product IDs from the returned dictionary.
        self.product_ids = list(self.products)

        # Number of products returned from search.
        self.number_of_products = len(self.product_ids)
        print(F"\n\n{self.number_of_products} products returned from search.")

        # Size of the total returned products.
        self.product_sizes = self.api.get_products_size(products=self.products)
        print(f"{self.product_sizes}GB worth of products will be downloaded.")

    def create_products_csv_file(self):
        """Create a .csv file from the metadata of products returned from the query."""
        geodataframe_products = self.api.to_geodataframe(self.products)

        metadata_file = r"metadatafile.csv"

        geodataframe_products.to_csv(path_or_buf=metadata_file, index=False)

        print("\n\nCreated a metadata file of all returned products. \n\tRefer to \"metadata.csv\" for detailed information.\n")

    def download_all_products(self):
        """Download all products returned from the search"""

        print("Downloading all products returned from the query.")
        download_directory = f"Downloaded Products/{self.start_time} to {self.end_time}"
        os.makedirs(name=download_directory, exist_ok=True)

        self.api.download_all(self.product_ids, directory_path=download_directory, checksum=True)


if __name__ == "__main__":
    DownloadData()
        