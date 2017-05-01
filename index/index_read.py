import csv
import sys
sys.path.append('../')
from db import DB
import datetime

header = list()
data = list()

db = DB()
conn = db.conn
cur = db.cur

def save_to_db(tuple_to_save):
	print tuple_to_save
	cur.execute('''insert ignore into 
		tomorrow_external_data.index_data(company, currency, date, value) 
		VALUES(%s,%s,%s,%s)''',tuple_to_save)
	print "New record saved:",tuple_to_save

with open("index_data.csv", 'rU') as csvfile:
	reader = csv.reader(csvfile)
	counter = 0
	for row in reader:
		if counter == 0:
			header = row[:len(row)-1]
		else:
			company = row[0]
			currency = row[1]
			for i in range(2, len(header)):
				dt = header[i]
				dt_arr = dt.split("/")
				year = "20"+str(dt_arr[2]);
				new_dt = datetime.date(int(year), int(dt_arr[1]),int(dt_arr[0]))
				val = row[i]
				tuple_to_save = (company, currency, new_dt.isoformat(), val)
				save_to_db(tuple_to_save)
			conn.commit()
		counter = counter + 1
cur.close()


