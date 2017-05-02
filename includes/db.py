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
