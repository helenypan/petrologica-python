import sys
sys.path.append('../includes')
from db import DB
import requests
import url_info
from bs4 import BeautifulSoup

db = DB()
conn = db.conn
cur = db.cur

def get_unit_well_link(unit):
	unit_id = unit[0]
	unit_name = unit[1]
	post_params = {
		"menu1" : "Unit",
		"menu3" : unit_name,
		"menu4" : "1/1971",
		"PrevU" : unit_name
	}
	resp = requests.post(url_info.unit_well_link_url,data=post_params,auth=(url_info.username, url_info.password)).content
	soup = BeautifulSoup(resp,'html.parser')
	tbl = soup.find_all("table")[1]
	rows = tbl.find_all("tr")
	for tr in rows:
		td = tr.find_all("td")[0]
		file_number = td.get_text()
		save_unit_well_link(unit_id, file_number)

def save_unit_well_link(unit_id, file_number):
	cur.execute('''
		insert ignore into tomorrow_wells_new.unit_well_links(UnitID, FileNo) values(%s, %s)
		''',(unit_id,file_number ))
	print("Record saved:",unit_id, file_number)



cur.execute('''
	select ID, UnitName from tomorrow_wells_new.units order by UnitName
	''')
counter = 0
for row in cur.fetchall():
	counter += 1
	get_unit_well_link(row)
	if counter % 50 ==0:
		conn.commit()
conn.commit()

		