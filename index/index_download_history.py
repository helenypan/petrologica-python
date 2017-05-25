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
url_to_complete = "https://uk.finance.yahoo.com/quote/{}/history?period1={}&period2={}&interval=1d&filter=history&frequency=1d"
url_ftse_history = "https://uk.investing.com/instruments/HistoricalDataAjax"

db = DB()
conn = db.conn
cur = db.cur

def get_date_after(t0, num_of_months):
	t = (t0 + datetime.timedelta(num_of_months*365/12)).strftime("%Y-%m-%d")
	return datetime.datetime.strptime(t, "%Y-%m-%d")

def get_seconds_from_date(t):
	return int((t - datetime.datetime(1970,1,1)).total_seconds())

def extract_ftse_history_data(url):
	ftse_data = {
	"action":"historical_data",
	"curr_id" : 27, 
	"st_date" : "01/01/2010",
	"end_date" : "25/05/2017",
	"interval_sec" : "Daily"
	}
	headers={
		"Host": "uk.investing.com",
		"Connection": "keep-alive",
		"Content-Length": "99",
		"Origin": "https://uk.investing.com",
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
		"Content-Type": "application/x-www-form-urlencoded",
		"Accept": "text/plain, */*; q=0.01",
		"X-Requested-With": "XMLHttpRequest",
		"Referer": "https://uk.investing.com/indices/uk-100-historical-data",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "en-GB,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2",
		"Cookie": "PHPSESSID=2hmbcb2a0u8hqatud9tigoltc7; adBlockerNewUserDomains=1495716248; \
gtmFired=OK; StickySession=id.2285927456.600uk.investing.com; \
optimizelyEndUserId=oeu1495716249369r0.9393955994124044; __qca=P0-439101783-1495716250288; \
__gads=ID=d8a4f97b263a533d:T=1495716250:S=ALNI_MZTjNmD4ydW5i2CNdF8xDdikCbNLQ; \
cookieConsent=was-set; geoC=GB; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A1%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A2%3A%2227%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A15%3A%22%2Findices%2Fuk-100%22%3B%7D%7D%7D%7D; optimizelySegments=%7B%224225444387%22%3A%22gc%22%2C%224226973206%22%3A%22direct%22%2C%224232593061%22%3A%22false%22%2C%225010352657%22%3A%22none%22%7D; optimizelyBuckets=%7B%7D; billboardCounter_51=1; nyxDorf=ODVhNGUtZTozZWFzZzM4Pzd4Yzk1NjY3; _ga=GA1.2.310379084.1495716250; _gid=GA1.2.1956065754.1495745779"
	}

	html = requests.post(url,data= ftse_data, headers= headers).content
	soup = BeautifulSoup(html,'html.parser')
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

def extract_company_history_prices(company_code, t0,t1):
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
		extract_company_history_prices(company_code, t0, t1)
		t0 = t1
		t1 = get_date_after(t0, month_gap)
		
# # now need to extract ftse100 data of the dates in dates_to_extract
extract_ftse_history_data(url_ftse_history)
cur.close()
