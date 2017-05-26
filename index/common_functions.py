import datetime
from bs4 import BeautifulSoup
import re

def get_date_after(t0, num_of_months):
	t = (t0 + datetime.timedelta(num_of_months*365/12)).strftime("%Y-%m-%d")
	return datetime.datetime.strptime(t, "%Y-%m-%d")

def get_seconds_from_date(t):
	return int((t - datetime.datetime(1970,1,1)).total_seconds())


def parse_company_prices(company_code, html,db):
	soup = BeautifulSoup(html, "html.parser")
	tbl_list = soup.find_all('table')
	for tbl in tbl_list:
		data_test_lbl = tbl.get("data-test")
		if data_test_lbl == "historical-prices":
				#found the data
			rows = tbl.find_all("tr")
			for row in rows:
				cells = row.find_all("td")
				if len(cells)== 7:
					dt_text = cells[0].getText()
					dt = str(datetime.datetime.strptime(dt_text,"%d %b %Y")).split()[0]
					open_val = float(cells[1].getText())
					close_val = float(cells[4].getText())
					volume_cal = re.sub(r'[,-]', '', cells[6].getText())
					if volume_cal:
						volume_cal = int(volume_cal)
					else:
						volume_cal = 0
					db.save_company_prices((company_code,dt,open_val, close_val,volume_cal))
			db.exe_commit()


def parse_ftse_prices(html, db):
	soup = BeautifulSoup(html,'html.parser')
	tbl_list = soup.find_all("table")
	for tbl in tbl_list:
		tbl_id = tbl.get("id")
		if tbl_id == "curr_table":
			rows = tbl.find_all("tr")
			for row in rows:
				cells = row.find_all("td")
				if len(cells) == 7:
					dt_text = cells[0].getText()
					index_data = cells[1].getText()
					index_val = float(re.sub(',', '', index_data))
					dt = str(datetime.datetime.strptime(dt_text,"%b %d, %Y")).split()[0]
					db.save_index_prices(("FTSE100",dt, index_val))
			db.exe_commit()