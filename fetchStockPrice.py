#! python3
# fetchStockPrice.py - Fetches the price of ICICI bank stock from icicidirect.com

import requests, bs4
res = requests.get('https://getquote.icicidirect.com/trading_stock_quote.aspx?Symbol=ICIBAN')
res.raise_for_status()

# TODO: Retrieve top search result links.
soup = bs4.BeautifulSoup(res.text, features="html.parser")

# TODO: Open a browser tab for each result.
linkElems = soup.select('div #NewHide > table > tr > td')

print(linkElems[1].getText().strip())

