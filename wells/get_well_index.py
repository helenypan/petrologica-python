import sys
sys.path.append('../includes')
from db import DB
from io import BytesIO
from io import TextIOWrapper
import requests
from zipfile import ZipFile
import csv
from datetime import datetime
import url_info

db = DB()
conn = db.conn
cur = db.cur


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

url_file = requests.get(url_info.well_index_url, auth=(url_info.username, url_info.password)).content
zip_file = ZipFile(BytesIO(url_file))
file_name = zip_file.namelist()[0]
item_file = TextIOWrapper(zip_file.open(file_name,"r"))

reader = csv.DictReader(item_file)
counter = 0 
for row in reader:
	update_well_index_in_db(row)
	counter += 1
	if counter % 50 == 0:
		conn.commit()
conn.commit()
cur.close()
		
  	

# for idx, row in enumerate(csv.DictReader(item_file)):
#     print('Processing row {0} -- row = {1}'.format(idx, row))


# with zip_file.open(file_name,"r") as f:
# 	reader = csv.reader(f)
# 	your_list = list(reader)
# print(your_list[:5])
