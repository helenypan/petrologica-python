import sys
sys.path.append('../includes')
from db import DB
import requests
from datetime import datetime
import url_info
import os
import csv

sess = requests.Session()
r = sess.get(url_info.login_url)
my_csrf_token = r.cookies['csrftoken']
data_login = {
	"csrfmiddlewaretoken": my_csrf_token,
	"username": url_info.username,
	"password": url_info.password,
}

headers_login = {
	"Referer":url_info.login_url
}

data_tracker = {
	"format":"csv"
}

headers_tracker = {
	"Referer":url_info.tracker_url_refer
}

sess.post(url_info.login_url,data=data_login, headers = headers_login)
res = sess.get(url_info.tracker_url,data=data_tracker, headers = headers_tracker )

cur_time  = datetime.now().strftime("%Y%m%dH%H")
file_name = "./archive/" + cur_time + ".csv"
dir_name =  os.path.dirname(file_name)
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

with open(file_name, 'wb') as f:
	f.write(res.content)

# read csv to db
db = DB()
conn = db.conn
cur = db.cur

with open(file_name, 'rU') as csv_file:
	reader = csv.reader(csv_file)
	counter = 0
	date_index_arr = [10,11,13,17]
	for row in reader:
		if counter == 0:
			pass
		else:
			for idx in date_index_arr:
				if row[idx]:
					row[idx] = row[idx].split()[0]
				else:
					row[idx] = None
			curr_record = tuple(row)
			cur.execute('''
			insert ignore into tomorrow_LNG.fleet_mon(Name, Flag, FlagISO2, IMO, MMSI, Callsign,
			Type, PhotoURL, LastPort, LastPortLOCODE, LastPortArrival, LastPortDeparture,
			LastEvent, LastEventTime, Destination, DestinationPort, DestinationPortLOCODE,
			ETA, Latitude, Longitude, Speed, Course, Location, Comment, Tags, FleetMonURL)
			VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
			''', curr_record)
			print("Record NO.{} Saved:".format(counter),curr_record)
		counter = counter + 1
		if counter % 50 == 0:
			conn.commit()
	conn.commit()
cur.close()