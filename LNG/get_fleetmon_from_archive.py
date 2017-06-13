import sys
sys.path.append('../includes')
from db import DB
import os
import csv

# read csv to db
db = DB()
conn = db.conn
cur = db.cur

def read_csv(csv_file):
	reader = csv.reader(csv_file)
	counter = 0
	date_index_arr = [10, 11, 13, 17]
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
			cur.execute('''insert ignore into tomorrow_LNG.fleet_mon(Name, Flag, FlagISO2, IMO, MMSI, Callsign,
    		   			Type, PhotoURL, LastPort, LastPortLOCODE, LastPortArrival, LastPortDeparture,
    		   			LastEvent, LastEventTime, Destination, DestinationPort, DestinationPortLOCODE,
    		   			ETA, Latitude, Longitude, Speed, Course, Location, Comment, Tags, FleetMonURL)
    		   			VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    		   			''', curr_record)
			print("Record NO.{} Saved:".format(counter), curr_record)
		counter = counter + 1
		if counter % 50 == 0:
			conn.commit()
	conn.commit()


directory = "./archive"
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".csv"):
            file_path = directory + "/" + file
            with open(file_path, 'rU') as csv_file:
                try:
                    read_csv(csv_file)
                except:
                    print("Failed to read:",file_path)
                    continue
cur.close()