import sys
sys.path.append('../includes')
from db import DB
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
import url_info
from bs4 import BeautifulSoup
from datetime import datetime

class MyAdapter(HTTPAdapter):
	def init_poolmanager(self, connections, maxsize, block=False):
		self.poolmanager = PoolManager(num_pools=connections,
										maxsize=maxsize,
										block=block,
										ssl_version=ssl.PROTOCOL_TLSv1)

db = DB()
conn = db.conn
cur = db.cur

def get_well_data(file_number):
	post_params = {
		"FileNumber" : file_number
	}
	s = requests.Session()
	s.mount("https://", MyAdapter())
	resp = s.post(url_info.well_prod_url,data=post_params,auth=(url_info.username, url_info.password)).content
	soup = BeautifulSoup(resp,'html.parser')

	tbl_summary = soup.find("table",{"summary":"Well data content table"})
	if tbl_summary:
		summary = tbl_summary.find("tr").find("div")
		year = datetime.today().year
		month = datetime.today().month
		cur.execute('''
			insert ignore into tomorrow_wells_new.well_monthly_summary(FileNo, Year, Month, Summary)
			values(%s, %s,%s, %s)''',(file_number,year, month, summary))
		print("Monthly summary saved for FileNo:",file_number)
	else:
		print("No summary available for FileNo:",file_number)

	tbl_prod = soup.find("table",{"id":"largeTableOutput"})
	if tbl_prod:
		rows = tbl_prod.find_all("tr")
		has_production_to_save = False
		for tr in rows:
			cells = tr.find_all("td")
			pool = cells[0].get_text()
			if pool != "Pool":
				dt = cells[1].get_text()
				year = int(dt.split("-")[1])
				month = int(dt.split("-")[0])
				if year >= 2005:
					prod_tuple = (file_number,pool, dt, year, month,\
						cells[2].get_text(),cells[3].get_text(),cells[4].get_text(),cells[5].get_text(),\
						cells[6].get_text(),cells[7].get_text(),cells[8].get_text() )
					cur.execute('''
						insert ignore into tomorrow_wells_new.well_production(FileNo,Pool,Date,Year, Month,
						Days, BBLSOil, Runs, BBLSWater, MCFProd,MCFSold, VentFlare) values
						(%s, %s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s)''',prod_tuple)
					has_production_to_save = True
		if has_production_to_save:
			print("Production saved for FileNo:",file_number)
		else:
			print("No Production after 2005 to be saved for FileNo:",file_number)
	else:
		print("No production data avaialbe for FileNo:",file_number)

	print("\n")
	conn.commit()


# get_well_data(30890)

cur.execute('''select FileNo from tomorrow_wells_new.well_index where FileNo not in 
	(select FileNo from tomorrow_wells_new.well_monthly_summary where Year=YEAR(CURDATE()) and Month = MONTH(CURDATE()))
	order by FileNo''')
for row in cur.fetchall():
	file_number = row[0]
	get_well_data(file_number)
cur.close()