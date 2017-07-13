import sys
sys.path.append('../includes')
from db import DB
from common_functions import parse_company_prices, parse_ftse_prices, get_seconds_from_date,get_date_after,parse_currency
import datetime
import urllib.request
import requests
import ssl
import re
context = ssl._create_unverified_context()

url_to_complete = "https://uk.finance.yahoo.com/quote/{}/history?period1={}&period2={}&interval=1d&filter=history&frequency=1d"
url_ftse_history = "https://uk.investing.com/instruments/HistoricalDataAjax"
url_currency_history = "https://www.investing.com/instruments/HistoricalDataAjax"

db = DB()
month_gap = 4

def extract_company_history_prices(company_code, t0,t1):
	t0_seconds = get_seconds_from_date(t0)
	t1_seconds = get_seconds_from_date(t1)
	url = url_to_complete.format(company_code,t0_seconds,t1_seconds)
	with urllib.request.urlopen(url, context=context) as url_file:
		html = url_file.read()
		parse_company_prices(company_code,html, db)


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
	parse_ftse_prices(html, db)

def extrace_currency_history_data(url, currency):
	currency_data = {
		"action":"historical_data",
		"curr_id":"37",
		"st_date":"01/01/2014",
		"end_date":"05/26/2017",
		"interval_sec":"Daily"
	}
	headers = {
		"Host": "www.investing.com",
		"Connection": "keep-alive",
		"Content-Length": "99",
		"Origin": "https://www.investing.com",
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/58.0.3029.110 Safari/537.36",
		"Accept": "text/plain, */*; q=0.01",
		"X-Requested-With": "XMLHttpRequest",
		"Referer": "https://www.investing.com/currencies/eur-nok-historical-data",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "en-GB,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2",
		"Cookie": "adBlockerNewUserDomains=1495716248; optimizelyEndUserId=oeu1495716249369r0.9393955994124044; \
__qca=P0-439101783-1495716250288; __gads=ID=d8a4f97b263a533d:T=1495716250:S=ALNI_MZTjNmD4ydW5i2CNdF8xDdikCbNLQ; \
PHPSESSID=e7qif9lociv41eic4r0ohse5h1; geoC=GB; gtmFired=OK; StickySession=id.80697086445.433www.investing.com; \
editionPostpone=1495790778437; \
SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A\
%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A1%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A2%3A\
%2237%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A20%3A%22Euro+Norwegian+Krone%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%\
2Fcurrencies%2Feur-nok%22%3B%7D%7D%7D%7D; optimizelySegments=%7B%224225444387%22%3A%22gc%22%2C%224226973206%22%3A%22direct\
%22%2C%224232593061%22%3A%22false%22%2C%225010352657%22%3A%22none%22%7D; optimizelyBuckets=%7B%7D; billboardCounter_1=2;\
 nyxDorf=NTg1Z2EpNWg%2FbWlkMn83NzVlM243Ljo6NzdjaA%3D%3D; _gat=1; _gat_allSitesTracker=1; _ga=GA1.2.310379084.1495716250; \
 _gid=GA1.2.1374619376.1495797462"
	}
	html = requests.post(url,data= currency_data, headers= headers).content
	parse_currency(html, db, currency)



db.cur.execute('''select company_code from tomorrow_external_data.index_company WHERE category ="OSEAX"; ''')
for row in db.cur.fetchall():
	company_code = row["company_code"]
	t0 = datetime.datetime(2014, 1, 1)
	t1 = get_date_after(t0, month_gap)
	while(t0 < datetime.datetime.now()):
		extract_company_history_prices(company_code, t0, t1)
		t0 = t1
		t1 = get_date_after(t0, month_gap)
		
# retrieve ftse 100 data
# extract_ftse_history_data(url_ftse_history)
# retrieve eur_nok currency data
# extrace_currency_history_data(url_currency_history, "EUR_NOK")
db.close_connection()