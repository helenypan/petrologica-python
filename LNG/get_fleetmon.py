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
file_name = "./archive/" + cur_time + ".html"
dir_name =  os.path.dirname(file_name)
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

s = requests.Session() 
data={"username":url_info.username, "password":url_info.password}
r1 = s.post(url_info.login_url,data=data)
response = s.get(url_info.tracker_url,data=data, cookies=r1.cookies)
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
		
  	
