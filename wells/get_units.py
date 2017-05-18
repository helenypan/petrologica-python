import sys
sys.path.append('../includes')
from db import DB
from bs4 import BeautifulSoup

db = DB()
conn = db.conn
cur = db.cur

def save_unit_name(unit_name):
	cur.execute('''insert ignore into 
		tomorrow_wells_new.units(UnitName) 
		VALUES(%s)''',(unit_name,))
	print("New unit saved:",unit_name)

html = open("unit_names.html").read()
soup = BeautifulSoup(html,'html.parser')
options = soup.find_all("option")
for option in options:
	unit_name = option.getText().strip()
	save_unit_name(unit_name);
conn.commit()
cur.close()

