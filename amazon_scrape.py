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

# Get product title
title = soup.find(id='productTitle').get_text().strip()

# Get price of product but if there is no price then this will prevent crashing
try:
    price = float(soup.find(id='priceblock_saleprice').get_text().replace('$', '').replace(',', '').strip())
except:
    price = ''

# Get review score out of 5 of the product
review_score = float(soup.select('.a-star-4-5')[0].get_text().split(' ')[0].replace(",", "."))

# Get how many reviews the product has
review_count = int(soup.select('#acrCustomerReviewText')[0].get_text().split(' ')[0].replace(",", ""))

# Getting the stock state and determining whether the product is in stock
try:
    soup.select('#availability .a-color-state')[0].get_text().strip()
    stock = 'Out of Stock'
except:
    stock = 'Available'

print(title)
print(price)
print(str(review_score) + ' out of ' + str(review_count) + ' reviews')
print(stock)