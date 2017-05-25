import sys
sys.path.append('../includes')
from db import DB
import datetime
from bs4 import BeautifulSoup
import urllib.request
import requests
import ssl
import re
context = ssl._create_unverified_context()
url_to_complete = "https://uk.finance.yahoo.com/quote/BP/history?interval=1d&filter=history&frequency=1d"
url_ftse_current = "https://uk.investing.com/indices/uk-100-historical-data"


db = DB()
conn = db.conn
cur = db.cur

def extract_ftse_current_data(url):
	req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	with urllib.request.urlopen(req, context = context) as url_file:
		html = str(url_file.read())
		html_list = re.split("<html |</html>",html)
		html_to_parse = "<html " + html_list[1] + "</html>"
		soup = BeautifulSoup(html_to_parse,'html.parser')
		tbl_list = soup.find_all("table")
		for tbl in tbl_list:
			tbl_id = tbl.get("id")
			if tbl_id == "curr_table":
				rows = tbl.find_all("tr")
				for row in rows:
					cells = row.find_all("td")
					if len(cells) == 7:
						dt_text = cells[0].getText()
						index_data = cells[1].getText()
						index_val = float(re.sub(',', '', index_data))
						dt = str(datetime.datetime.strptime(dt_text,"%b %d, %Y")).split()[0]
						save_to_db("FTSE100",dt, index_val)
	conn.commit()


def save_to_db(company_code, dt, val):
	cur.execute('''insert ignore into 
		tomorrow_external_data.index_data(company_code, date, value) 
		VALUES(%s,%s,%s)''',(company_code, dt, val))
	print("New record saved:",(company_code, dt, val))

def extract_company_current_prices(company_code):
	url = url_to_complete.format(company_code)
	with urllib.request.urlopen(url, context=context) as url_file:
		html = url_file.read()
		soup = BeautifulSoup(html, "html.parser")
		tbl_list = soup.find_all('table')
		for tbl in tbl_list:
			data_test_lbl = tbl.get("data-test")
			if data_test_lbl == "historical-prices":
				#found the data
				rows = tbl.find_all("tr")
				for row in rows:
					cells = row.find_all("td")
					if len(cells)== 7:
						dt_text = cells[0].getText()
						close_val = float(cells[4].getText())
						dt = str(datetime.datetime.strptime(dt_text,"%d %b %Y")).split()[0]
						save_to_db(company_code,dt, close_val)
		conn.commit()


cur.execute('''select company_code from 
	tomorrow_external_data.index_company''')
for row in cur:
	company_code = row[0]
	extract_company_current_prices(company_code)
		
# # now need to extract ftse100 data 
extract_ftse_current_data(url_ftse_current)
cur.close()
