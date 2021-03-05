import requests
from glob import glob
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from time import sleep

# Common User Agent to emulate Chrome
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

# Import the CSV file that contain's the product URL's
prod_tracker = pd.read_csv('trackers/product_tracker.csv', sep=';')
prod_tracker_URLS = prod_tracker.url

# Get the URL
page = requests.get(prod_tracker_URLS[0], headers=HEADERS)

# Create a `soup` object that makes processing the HTML much easier
soup = BeautifulSoup(page.content, features="lxml")