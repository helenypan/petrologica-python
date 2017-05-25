import sys
sys.path.append('../includes')
from db import DB
from io import BytesIO
from io import TextIOWrapper
import requests
import csv
from datetime import datetime
import url_info
import os

# db = DB()
# conn = db.conn
# cur = db.cur


def update_well_index_in_db(row):
	well_number = row['FileNo']
	cur.execute('''delete from 
		tomorrow_wells_new.well_index where FileNo = %s''',(well_number,))
	sql = "insert into tomorrow_wells_new.well_index set"
	for idx, val in row.items():
		if idx == "SpudDate" or idx == "WellStatusDate":
			# need to convert the format of the date
			if "/" in val:
				dt_obj = datetime.strptime(val, '%m/%d/%Y')
				val = dt_obj.strftime("%Y-%m-%d")
			else:
				val = None
		else:
			val = val.replace('"','')
		sql += ' `{}` = "{}",'.format(idx, val)
	sql = sql.strip(",")
	cur.execute(sql)
	# if well_number == "15":
	# 	print(sql)
	print("Well saved:",well_number)


cur_time  = datetime.now().strftime("%Y%m%dH%H")
file_name = "./archive/" + cur_time + ".csv"
dir_name =  os.path.dirname(file_name)
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

headers ={
	"Host": "www.fleetmon.com",
	"Connection": "keep-alive",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Referer": "https://www.fleetmon.com/my/vessels/",
	"Accept-Encoding": "gzip, deflate, sdch, br",
	"Accept-Language": "en-GB,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2",
	"Cookie": "intercom-id-kwshk9to=f237a359-ceff-48fa-8ecd-511b1b78f407; _hjIncludedInSample=1;\
csrftoken=Q8L2H0vKLlI5dcLeiaiXqVdH63RKGMSb; ajs_anonymous_id=null; \
_ga=GA1.2.373668620.1495546644; _gid=GA1.2.846791572.1495747134; _gat=1;\
intercom-session-kwshk9to=cWlTVmVkbTAyMkxCRDhuSU1mVlFsOE94Q3duMmRjcTM3NXFtR2lJd0ErU1hJMGVqc0dsbUtMZytkQnlqWGE3bC0tV2d1eEFqSTZ4QWhtWHRPa1dncHBBUT09--ea2808ba991daa5ba1d8f8e82bcd9b744a3dc762;\
fmc_session=6aqgobkyg8ehxm9skcy4skl8ct1itzt0; _gali=download-export-module"
}



# s = requests.Session() 
# data={"username":url_info.username, "password":url_info.password}
# r1 = s.post(url_info.login_url,data=data)
response = requests.get(url_info.tracker_url,headers=headers)
with open(file_name, 'wb') as f:
	f.write(response.content)

# zip_file = ZipFile(BytesIO(url_file))
# file_name = zip_file.namelist()[0]
# item_file = TextIOWrapper(zip_file.open(file_name,"r"))

# reader = csv.DictReader(item_file)
# counter = 0 
# for row in reader:
# 	update_well_index_in_db(row)
# 	counter += 1
# 	if counter % 50 == 0:
# 		conn.commit()
# conn.commit()
# cur.close()
		
  	
