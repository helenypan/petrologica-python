import sys
sys.path.append('../includes')

from db import DB
import re

def save_to_db(row_list):
	row_tuple = tuple(row_list)
	cur.execute('''insert into field_onshore_map(primkey, country, country_id, basin, basin_id,
		project, project_id, field_id, otherinfo,lat, lng, resinfo, disc, prod, fipscode, cowcode,
		contcode, sitenum, res, locsource, fieldinfo, discpres,prodpres,sourceinfo)VALUES
		(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
		''', row_tuple)
	print "Record saved:",row_tuple


db = DB()
conn = db.conn
cur = db.cur

cur.execute('''select primkey, country, country_id, basin, basin_id,
		project, project_id, field_id, otherinfo,lat, lng, resinfo, disc, prod, fipscode, cowcode,
		contcode, sitenum, res, locsource, fieldinfo, discpres,prodpres,sourceinfo
		 from field_onshore_map where Locate(",", project)>0 or Locate(" and ", project)>0''')
for row in cur.fetchall():
	row_list = list(row)
	cur_project = row[5]
	cur_project_arr = re.split(',| and ', cur_project)
	for each in cur_project_arr:
		each = each.strip()
		row_list[5] = each
		# print len(row_list)
		save_to_db(row_list)
	cur.execute('delete from field_onshore_map where project =%s',(cur_project,))
	print "orginal record deleted:",row
	conn.commit()




