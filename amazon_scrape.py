import requests
import argparse
import yagmail
from glob import glob
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from time import sleep

# Common User Agent to emulate Chrome
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

# The gmail account you will use to send emails (you can use your own or make a development email)
GMAIL_USERNAME = ''


def search_product_list(email, interval_count=1, interval_hours=1):
    '''
    Returns whether a product is in stock, if the price is underneath a user-specified amount, and whether to buy or not.

            Parameters:
                    email (string): Required, the email to send a notification to if the product is in stock and under the price threshold
                    interval_count (int): Optional, defaults to 1, the number of times the script should run
                    interval_hours (int): Optional, defaults to 1, the number of hours between each run of the script

            Returns:
                    No return from function but outputs a spreadsheet logging product info for each run of the script.
    '''

    # Import the CSV file that contain's the product URL's
    prod_tracker = pd.read_csv('trackers/product_tracker.csv', sep=';')
    prod_tracker_URLS = prod_tracker.url
    tracker_log = pd.DataFrame()
    now = datetime.now().strftime('%Y-%m-%d %Hh%Mm')
    interval = 0

    while interval < interval_count:
        for x, url in enumerate(prod_tracker_URLS):
            # Get the URL
            page = requests.get(url, headers=HEADERS)

            # Create a `soup` object that makes processing the HTML much easier
            soup = BeautifulSoup(page.content, features="lxml")

            # Get product title
            title = soup.find(id='productTitle').get_text().strip()

            # Get price of product but if there is no price then this will prevent crashing
            try:
                price = float(soup.find(id='priceblock_saleprice').get_text().replace(
                    '$', '').replace(',', '').strip())
            except:
                price = ''

            # Get the review score and review count and also check alternate location on page
            try:
                review_score = float(soup.select(
                    '.a-star-4-5')[0].get_text().split(' ')[0].replace(",", "."))
                review_count = int(soup.select('#acrCustomerReviewText')[
                                   0].get_text().split(' ')[0].replace(",", ""))
            except:
                try:
                    review_score = float(soup.select(
                        'i[class*="a-icon a-icon-star a-star-"]')[1].get_text().split(' ')[0].replace(",", "."))
                    review_count = int(soup.select('#acrCustomerReviewText')[
                                       0].get_text().split(' ')[0].replace(",", ""))
                except:
                    review_score = ''
                    review_count = ''

            # Getting the stock state and determining whether the product is in stock and also checking alternate location
            try:
                soup.select(
                    '#availability .a-color-state')[0].get_text().strip()
                stock = 'Out of Stock'
            except:
                try:
                    soup.select(
                        '#availability .a-color-price')[0].get_text().strip()
                    stock = 'Out of Stock'
                except:
                    stock = 'Available'

            # Gather all the information when this script is run so we can log it and track its history.
            log = pd.DataFrame({'date': now.replace('h', ':').replace('m', ''),
                                # this code comes from the TRACKER_PRODUCTS file
                                'code': prod_tracker.code[x],
                                'url': url,
                                'title': title,
                                # this price comes from the TRACKER_PRODUCTS file
                                'buy_below': prod_tracker.buy_below[x],
                                'price': price,
                                'stock': stock,
                                'review_score': review_score,
                                'review_count': review_count}, index=[x])

            # If the price is below the threshold, send user email, otherwise, skip this step!
            try:
                if price < prod_tracker.buy_below[x]:
                    print(
                        title + '\nItem above is below price threshold, sending email!')
                    yagmail.SMTP(GMAIL_USERNAME).send(email,
                                                      'Item(s) on List Available!', 'Item: ' + title + ' available!' + '\n' + url)
            except:
                print(title + '\nItem above is out of stock or above price threshold!')
                pass

            # Append the gathered information to a log file
            tracker_log = tracker_log.append(log)
            print('\nAppended ' + prod_tracker.code[x] + '\n')
            sleep(5)

        interval += 1

        # Since the sleep function uses seconds by default, we must multiply by 3600 to convert hours to seconds
        sleep(interval_hours*3600)
        print('End of Interval ' + str(interval) + '\n\n')

    # Find the last log file and create new log file with new logging data
    last_search = glob(
        '/Users/subal/Documents/Dev/Senior/Winter Intensive/IsItStocked/search_history/*.xlsx')[-1]
    search_hist = pd.read_excel(last_search)
    final_df = search_hist.append(tracker_log, sort=False)

    final_df.to_excel(
        'search_history/SEARCH_HISTORY_{}.xlsx'.format(now), index=False)
    print('\nEnd of Lookup.')


if __name__ == '__main__':
    # Initalize command line argument parser
    parser = argparse.ArgumentParser()

    # Add long and short argument
    parser.add_argument("-i", "--interval",
                        help="*OPTIONAL* - determine how many times script should run")
    parser.add_argument("-s", "--sleep",
                        help="*OPTIONAL* - determine how many hours between each run of script")
    parser.add_argument("-e", "--email",
                        help="*REQUIRED* - enables script to send user email")

    # Read arguments from the command line
    args = parser.parse_args()

    # Check for command line arguments
    if args.email:
        if args.interval:
            if args.sleep:
                search_product_list(args.email, int(
                    args.interval), int(args.sleep))
            else:
                search_product_list(args.email, int(args.interval))
        else:
            if args.sleep:
                search_product_list(args.email, 1, int(args.sleep))
            else:
                search_product_list(args.email)
    else:
        print("Please use -e or --email followed by your email!")
