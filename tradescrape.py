# Import Required Libraries
import yahooquery as yq # Pull Historical and Financial Data on Tickers
import pandas as pd # Manage database
import requests # Request HTML Sites for Scraping
from bs4 import BeautifulSoup # Webscraping functions

# Webpage to pull Stock Tickers from (in this case, TradingView All Canadian Stocks)
html = "https://www.tradingview.com/markets/stocks-canada/market-movers-all-stocks/"

#Define res as Request to HTML
res = requests.get(html)
#Parse Webpage Content
soup = BeautifulSoup(res.content, 'html.parser')
page_body = soup.body.encode('utf-8')
print(page_body)



ticker = "MSFT"
stock = yq.Ticker(ticker)
data = stock.financial_data
historical = stock.history(period='max')

stock_data= pd.DataFrame(stock_data)
stock_history = pd.DataFrame(historical)


print(stock_data)
