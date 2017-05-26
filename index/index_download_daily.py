import sys
sys.path.append('../includes')
from db import DB
from common_functions import parse_company_prices, parse_ftse_prices,parse_currency
import urllib.request
import ssl
import re
context = ssl._create_unverified_context()
url_to_complete = "https://uk.finance.yahoo.com/quote/BP/history?interval=1d&filter=history&frequency=1d"
url_ftse_current = "https://uk.investing.com/indices/uk-100-historical-data"
url_currency_current = "https://www.investing.com/currencies/eur-nok-historical-data"

db = DB()

def extract_ftse_current_data(url):
	req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	with urllib.request.urlopen(req, context = context) as url_file:
		html = str(url_file.read())
		html_list = re.split("<html |</html>",html)
		html_to_parse = "<html " + html_list[1] + "</html>"
		parse_ftse_prices(html_to_parse, db)

def extract_currency_current_data(url, currency):
	req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	with urllib.request.urlopen(req, context = context) as url_file:
		html = str(url_file.read())
		html_list = re.split("<html |</html>",html)
		html_to_parse = "<html " + html_list[1] + "</html>"
		parse_currency(html_to_parse, db,currency )


def extract_company_current_prices(company_code):
	url = url_to_complete.format(company_code)
	with urllib.request.urlopen(url, context=context) as url_file:
		html = url_file.read()
		parse_company_prices(company_code,html, db)



db.cur.execute('''select company_code from tomorrow_external_data.index_company;''')
for row in db.cur:
	company_code = row[0]
	extract_company_current_prices(company_code)
		
# extract ftse100 data 
extract_ftse_current_data(url_ftse_current)
# retrieve eur_nok currency data
extract_currency_current_data(url_currency_current,"EUR_NOK" )
db.close_connection()



