# Import Required Libraries
import yahooquery as yq # Pull Historical and Financial Data on Tickers
import pandas as pd # Manage database
import requests # Request HTML Sites for Scraping
from bs4 import BeautifulSoup # Webscraping functions
from itertools import *
import os

# Webpage to pull Stock Tickers from (in this case, TradingView All Canadian Stocks)
html = "https://www.tradingview.com/markets/stocks-canada/market-movers-all-stocks/"

# Define res as Request to HTML and Parse HTML Content
res = requests.get(html)
soup = BeautifulSoup(res.content, 'html.parser').prettify()

# Write Webpage Output to HTML File for Cleaning
pt = open("parsed_text.html", "wb")
pt.write(soup.encode('utf-8'))
pt.close()

#Iterate Over HTML to Remove Useless Lines
with open("parsed_text.html", "r") as input:
    with open("parsed_text_clean1.html", "w") as output:
        for line in input:
            if "data-rowkey" in line.strip("\n"):
                output.write(line)
                
with open("parsed_text_clean1.html", "r") as input:
    with open("parsed_text_clean2.html", "w") as output:
        for line in input:
            newline = line.strip('<tr class="row-RdUXZpkv listRow" data-rowkey=')
            output.write(newline)

with open("parsed_text_clean2.html", "r") as input:
    with open("parsed_text_clean3.html", "w") as output:
        for line in input:
            newline = line.strip('TSXV:')
            output.write(newline)





ticker = "MSFT"
stock = yq.Ticker(ticker)
data = stock.financial_data
historical = stock.history(period='max')

stock_data= pd.DataFrame(data)
stock_history = pd.DataFrame(historical)

print(stock_data.head(n=5))
print(stock_history.head(n=5))
