import sys
sys.path.append('../includes')
from db import DB
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
import ssl
import re
context = ssl._create_unverified_context()
url_to_complete = "https://uk.finance.yahoo.com/quote/{}/history?interval=1wk&filter=history&frequency=1wk"
url_ftse = "https://uk.investing.com/indices/uk-100-historical-data"

db = DB()
conn = db.conn
cur = db.cur

def extract_ftse_data(url, dates):
	req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	# html = urlopen(req,, context = context).read()
	with urllib.request.urlopen(req, context = context) as url_file:
		html = str(url_file.read())
		html_list = re.split("<html |</html>",html)
		html_to_parse = "<html " + html_list[1] + "</html>"
		# print(html_to_parse)
		soup = BeautifulSoup(html_to_parse,'html.parser')
		tbl_list = soup.find_all("table")
	for tbl in tbl_list:
		tbl_id = tbl.get("id")
		if tbl_id == "curr_table":
			rows = tbl.find_all("tr")
			counter = 0
			for row in rows:
				if counter >0 and counter <15:
					cells = row.find_all("td")
					dt_text = cells[0].getText()
					index_data = cells[1].getText()
					index_val = float(re.sub(',', '', index_data))
					dt = str(datetime.strptime(dt_text,"%b %d, %Y")).split()[0]
					if dt in dates:
						save_to_db("FTSE100",dt, index_val)
				counter = counter + 1
	conn.commit()


def save_to_db(company_code, dt, val):
	cur.execute('''insert ignore into 
		tomorrow_external_data.index_data(company_code, date, value) 
		VALUES(%s,%s,%s)''',(company_code, dt, val))
	print("New record saved:",(company_code, dt, val))

def extract_company_prices(url):
	dt_list = list()
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
				if counter >0 and counter < 3:
					cells = row.find_all("td")
					dt_text = cells[0].getText()
					close_val = float(cells[4].getText())
					dt = str(datetime.strptime(dt_text,"%d %b %Y")).split()[0]
					if dt not in dt_list:
						dt_list.append(dt)
					save_to_db(company_code,dt, close_val)
				counter = counter + 1
	conn.commit()
	return dt_list


company_codes = list()
dates_to_extract = None
cur.execute('''select company_code from 
	tomorrow_external_data.index_company''')
for row in cur.fetchall():
	company_codes.append(row[0])

for company_code in company_codes:
	url = url_to_complete.format(company_code)
	if dates_to_extract is None:
		dates_to_extract = extract_company_prices(url)
	else:
		extract_company_prices(url)
# now need to extract ftse100 data of the dates in dates_to_extract
extract_ftse_data(url_ftse,dates_to_extract)
cur.close()




