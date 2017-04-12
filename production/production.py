import db

class Production:
	def __init__(self, country_id, production_type, production, year, month):
		self.country_id = country_id
		if production_type == "Total Crude":
			self.production_type = "OilCond"
		elif production_type == "Offshore Crude":
			self.production_type = "OffshoreOilCond"
		elif production_type == "Onshore Crude":
			self.production_type = "OnshoreOilCond"
		elif production_type == "NGL":
			self.production_type = "NGL"
		else:
			self.production_type = "OtherLiquid"
		self.production = production
		self.year = year
		self.month = month

	def save_to_db(self):
		quarter = (self.month - 1) / 3 + 1
		sql = ('insert into prodCountry_final(CountryID, ' + self.production_type + ',Year, Quarter, Month)'
			'VALUES('+str(self.country_id) + ',' +  str(self.production) +',' + str(self.year) + 
			','+ str(quarter) +',' + str(self.month)+') '
			'on duplicate key update ' + self.production_type +'= '+ str(self.production))
		db.sql_update(sql)