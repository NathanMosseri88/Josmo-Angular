import sys
import os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import adal
import requests
import json
import pandas
from Database_Modules import print_color, map_module_setting, run_sql_scripts
import time


class PavoAPIClass():
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = self.set_headers()

    def set_headers(self):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Pavo-Token':  self.api_key  # Replace with the actual token
        }
        return headers

    def list_products(self):
        url = f'https://api.omspavo.com/products'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            print(data)
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            print(response.text)

    def get_image(self, image_name):
        url = f'https://api.omspavo.com/product/{image_name}/images'
        response = requests.get(url, headers=self.headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            print_color(data, color='y')
            if len(data.get("images").keys()) >0:
                image_link = data.get("images").get("__general").get("medium")[0]
            else:
                image_link = None
            return image_link
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            print(response.text)
            return None
