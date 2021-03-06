# Is It Stocked?

## What is it?
Is It Stocked is a console based web-scraping app that uses:
 - [Python 3](https://www.python.org/) (requires Python 3.8+!)
 - [Beautiful Soup](https://pypi.org/project/beautifulsoup4/)
 - [Pandas](https://pandas.pydata.org/)
 - [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/)
 - [Yagmail](https://github.com/kootenpv/yagmail)

Specifically, the application scrapes the webpages of products that the user can choose from [Amazon](https://www.amazon.com/) and notifies the user (via console and email) if a product is in stock and under a user-defined price threshold. This is useful for assisting users in purchasing products that are commonly out-of-stock and combatting scalpers. Currently, this application only supports Amazon in the USA.

## How to Install?
### Step 1:
Clone this repository.
```git
git clone https://github.com/soundreaper/IsItStocked.git
```
### Step 2:
Go into the new folder and setup a virtual environment.
```bash
cd IsItStocked

# If you don't have virtualenv, install it:
pip3 install virtualenv

# I chose "venv" for the virtual environment name, it can be anything.
virtualenv venv
source venv/bin/activate

# Should you need to leave the virtual environment:
deactivate
```
### Step 3:
Install all dependencies.
```bash
pip3 install requirements.txt
```
### Step 4:
For automated emailing to function, you must setup Yagmail first. I used my professional email to test all my code but I recommend making a development email with [Gmail](https://mail.google.com/). In any case, you must allow 3rd-party app access to your Gmail account. You can do this by logging into the Gmail account and the clicking your profile icon at the top right and clicking "Manage your Google Account". If asked, enter you password and when the dashboard loads, click on "Security" on the left. Scroll down and find "Less secure apps" and set this option to "YES". This will allow Yagmail to use the registered email.
```python
# Start your python interpreter in the console:
python3

Python 3.8.1 (v3.8.1:1b293b6006, Dec 18 2019, 14:08:53)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import yagmail
>>> yagmail.register('YOUR_GMAIL_USERNAME@gmail.com', 'YOUR_GMAIL_PASSWORD')
>>> exit()

'''
Your Gmail account information is now stored in the Mac OS Keychain. To
prevent any errors, press CMD + Space on your keyboard and type in "keychain"
and open up "Keychain Access.app". At the top right, search "yagmail" and you
should see the entry you just created. Double-click on it, go to the
"Access Control" tab and click the first option to allow all applications to
access this item. This is so that Python has access to this Keychain item and
doesn't cause any errors. If you wish to remove the item for security
reasons, right click on the entry in the Keychain app and delete it.
'''
```
### Step 5:
Open "amazon_scrape.py" in your favorite code editor.
```python
'''
Find this global constant and set this to the same Gmail name you
registered to Yagmail.
'''
GMAIL_USERNAME = 'YOUR_GMAIL_USERNAME@gmail.com'
```
### Step 6:
Go back to the console and now you are ready to run the application!

There are three different console arguments to use with the application:
| Argument | Required? | What does it do? |
|:-:|:-:|:-:|
| -e or --email | Yes | the email you wish to send stock notifications to |
| -i or --interval | No, default is 1 | the number of times for the script to run |
| -s or --sleep | No, default is 1 | the number of hours between each run of the script |

```bash
'''
This will run the script 5 times, with 2 hours between each run and
send an email to test@gmail.com if, during any of the runs, an item
is in stock and under the user-defined price threshold.
'''
python3 amazon_scrape.py -i 5 -s 2 -e test@gmail.com
```

## How to Configure Items Being Watched?
Within the project directory, there is a folder called "trackers" and a file called "product_tracker.csv". You can add links to products you wish to monitor here.

Open the CSV file with your favorite code editor.
```bash
'''
I have included 2 example items already. If you wish to change them, simply
find the product on Amazon, copy the link in the address bar and paste it below
the first line in the CSV file. Add a semi-colon and then find the "ASIN"
number of the item from the link. In the below example items, the ASIN numbers
are "B07B45D8WV" and "B08L8JNTXQ", respectively. Add anoher semi-colon and
then put the maximum price you would purchase the item for. You can then
save the file and close it.
'''
url;code;buy_below
https://www.amazon.com/Sony-Full-frame-Mirrorless-Interchangeable-Lens-ILCE7M3K/dp/B07B45D8WV/ref=sr_1_1?dchild=1&keywords=sony+a7&qid=1614905465&sr=8-1;B07B45D8WV;1900
https://www.amazon.com/ASUS-Graphics-DisplayPort-Axial-Tech-2-9-Slot/dp/B08L8JNTXQ/ref=sr_1_11?dchild=1&keywords=rtx+3080&qid=1614904662&sr=8-11;B08L8JNTXQ;780
```

## Search History
There is a folder within the directory called "search_history". Within the directory, is a file called "SEARCH_HISTORY.xlsx". **Do not edit or remove this file** as it is used the first time the application is run to generate future spreadsheets.

After running the application once, a new spreadsheet should appear in this folder with the same name but followed by the date and time. Every time the application is run and all runs are completed, a new spreadsheet logging information about each product will be generated.