import sys
sys.path.append('../includes')
from db import DB
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
import ssl
context = ssl._create_unverified_context()
url_to_complete = "https://uk.finance.yahoo.com/quote/{}/history?interval=1wk&filter=history&frequency=1wk"


db = DB()
conn = db.conn
cur = db.cur

def save_to_db(company_code, dt, val):
	cur.execute('''insert ignore into 
		tomorrow_external_data.index_data(company_code, date, value) 
		VALUES(%s,%s,%s)''',(company_code, dt, val))
	print("New record saved:",(company_code, dt, val))

def extract_company_prices(url):
	with urllib.request.urlopen(url, context=context) as url_file:
		html = url_file.read()
		soup = BeautifulSoup(html, "html.parser")
		tbl_list = soup.find_all('table')
	for tbl in tbl_list:
		data_test_lbl = tbl.get("data-test")
		if data_test_lbl == "historical-prices":
			#found the data
			rows = tbl.find_all("tr")
			counter = 0
			for row in rows:
				if counter >0 and counter < 5:
					cells = row.find_all("td")
					dt_text = cells[0].getText()
					close_val = float(cells[4].getText())
					dt = str(datetime.strptime(dt_text,"%d %b %Y")).split()[0]
					save_to_db(company_code,dt, close_val)
				counter = counter + 1
	conn.commit()


company_codes = list()
cur.execute('''select company_code from 
	tomorrow_external_data.index_company''')
for row in cur.fetchall():
	company_codes.append(row[0])

for company_code in company_codes:
	url = url_to_complete.format(company_code)
	extract_company_prices(url)
cur.close()




