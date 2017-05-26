import MySQLdb

class DB:
	host = '127.0.0.1'
	user = 'root'
	password = 'root'
	port = 3306
	db = 'tomorrow_nopex'

	conn = None
	cur = None

	def __init__(self):
		self.conn = MySQLdb.connect(
    	host=self.host,
    	user=self.user,
    	passwd=self.password,
    	port=self.port,
    	db=self.db
		)
		self.cur = self.conn.cursor()

	def save_index_prices(self, record):
		self.cur.execute('''insert ignore into 
			tomorrow_external_data.index_prices(index_name, date, price) 
			VALUES(%s,%s,%s)''',record)
		print("New record saved:",record)

	def save_currency(self, currency, record):
		self.cur.execute('''insert ignore into 
			tomorrow_external_data.currency(date,{}) 
			VALUES(%s,%s)'''.format(currency),record)
		print("New record saved:",currency, record)

	def save_company_prices(self,record):
		self.cur.execute('''insert ignore into 
			tomorrow_external_data.company_prices(company_code, date, open, close, volume) 
			VALUES(%s,%s,%s,%s,%s)''',record)
		print("New record saved:",record)

	def close_connection(self):
		self.cur.close()

	def exe_commit(self):
		self.conn.commit()

