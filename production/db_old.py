import MySQLdb

host = '127.0.0.1'
user = 'root'
password = 'root'
port = 3306
db = 'tomorrow_nopex'

conn = MySQLdb.Connection(
    host=host,
    user=user,
    passwd=password,
    port=port,
    db=db
)

def sql_update(sql):
	conn.query(sql)
	conn.commit

def sql_query(sql):
	conn.query(sql)
	result = conn.store_result()
	for i in range(result.num_rows()):
		print result.fetch_row()