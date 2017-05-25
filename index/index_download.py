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
# url_to_complete = "https://uk.finance.yahoo.com/quote/{}/history?interval=1wk&filter=history&frequency=1wk"
url_to_complete = "https://uk.finance.yahoo.com/quote/{}/history?period1={}&period2={}&interval=1d&filter=history&frequency=1d"
url_ftse = "https://uk.investing.com/indices/uk-100-historical-data"

db = DB()
conn = db.conn
cur = db.cur

def get_date_after(t0, num_of_months):
	t = (t0 + datetime.timedelta(num_of_months*365/12)).strftime("%Y-%m-%d")
	return datetime.datetime.strptime(t, "%Y-%m-%d")

def get_seconds_from_date(t):
	return int((t - datetime.datetime(1970,1,1)).total_seconds())


def extract_ftse_data(url):
	# data = {"st_date":"25/04/2010","end_date":"25/05/2011"}
	# req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	# # html = urlopen(req,, context = context).read()
	# with urllib.request.urlopen(req, context = context) as url_file:
	# 	html = str(url_file.read())
	# 	html_list = re.split("<html |</html>",html)
	# 	html_to_parse = "<html " + html_list[1] + "</html>"
	# 	# print(html_to_parse)
	# 	soup = BeautifulSoup(html_to_parse,'html.parser')
	# 	tbl_list = soup.find_all("table")
	data = {"st_date":"25/04/2010","end_date":"25/05/2011"}
	html = requests.post(url,params= data ).content
	# html_list = re.split("<html |</html>",html)
	# html_to_parse = "<html " + html_list[1] + "</html>"
	print(html)
	# soup = BeautifulSoup(html_to_parse,'html.parser')
	# tbl_list = soup.find_all("table")
	# for tbl in tbl_list:
	# 	tbl_id = tbl.get("id")
	# 	if tbl_id == "curr_table":
	# 		rows = tbl.find_all("tr")
	# 		for row in rows:
	# 			cells = row.find_all("td")
	# 			print(len(cells))
	# 			if len(cells) == 7:
	# 				dt_text = cells[0].getText()
	# 				index_data = cells[1].getText()
	# 				index_val = float(re.sub(',', '', index_data))
	# 				dt = str(datetime.datetime.strptime(dt_text,"%b %d, %Y")).split()[0]
	# 				save_to_db("FTSE100",dt, index_val)
	# conn.commit()


def save_to_db(company_code, dt, val):
	cur.execute('''insert ignore into 
		tomorrow_external_data.index_data(company_code, date, value) 
		VALUES(%s,%s,%s)''',(company_code, dt, val))
	print("New record saved:",(company_code, dt, val))

def extract_company_prices(company_code, t0,t1):
	t0_seconds = get_seconds_from_date(t0)
	t1_seconds = get_seconds_from_date(t1)
	url = url_to_complete.format(company_code,t0_seconds,t1_seconds)
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


month_gap = 4
company_codes = list()
dates_to_extract = None
cur.execute('''select company_code from 
	tomorrow_external_data.index_company''')
for row in cur:
	company_code = row[0]
	t0 = datetime.datetime(2010, 1, 1)
	t1 = get_date_after(t0, month_gap)
	while(t0 < datetime.datetime.now()):
		extract_company_prices(company_code, t0, t1)
		t0 = t1
		t1 = get_date_after(t0, month_gap)
		
# now need to extract ftse100 data of the dates in dates_to_extract
# extract_ftse_data(url_ftse)
cur.close()
