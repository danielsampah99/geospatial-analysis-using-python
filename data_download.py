# data download.py

# Importing necessary modules.
from sentinelsat import (SentinelAPI, geojson_to_wkt, read_geojson)
from datetime import datetime, date
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
        print("Connecting to Sentinel API...")
        self.api = SentinelAPI(user=self.username, 
                    password=self.password, 
                    api_url=self.api_url, 
                    show_progressbars=True, 
                    timeout=300)
        print("Successfully connected to the API")
        
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
        self.start_time = date(year=2023, month=3, day=1)
        self.end_time = date(year=2023, month=3, day=20)

        "The options for area relation include {'Intersects', 'Contains', 'IsWithin'} and are all case sensitive."

        self.products = self.api.query(area=self.footprint, 
                                       date=(self.start_time, self.end_time), 
                                       area_relation="IsWithin", 
                                       cloudcoverpercentage=(0, 10), 
                                       platformname="Sentinel-2", 
                                    #    producttype="S2MSI2A"
                                    )
        
        # Create a list of product IDs from the returned dictionary.
        self.product_ids = list(self.products)

        # Number of products returned from search.
        self.number_of_products = len(self.product_ids)
        print(F"{self.number_of_products} number of products returned from search")

        # Size of the total returned products.
        self.product_sizes = self.api.get_products_size(products=self.products)
        print(f"{self.product_sizes} worth of products will be downloaded.")

    def create_products_csv_file(self):
        """Create a .csv file from the metadata of products returned from the query."""
        print(f"Creating a metadata file of the returned products.\n\n")
        geodataframe_products = self.api.to_geodataframe(self.products)

        metadata_file = r"metadatafile.csv"

        geodataframe_products.to_csv(path_or_buf=metadata_file, index=False)

        print("Successfully created metadata.csv")

    def download_all_products(self):
        """Download all products returned from the search"""

        print("Downloading all products returned fromt the query.")
        download_destination = os.makedirs(name=f"{self.start_time} to {self.end_time}", exist_ok=True)

        self.api.download(id=self.product_ids, directory_path=download_destination, checksum=True)


if __name__ == "__main__":
    DownloadData()
        