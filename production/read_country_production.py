from openpyxl import load_workbook

wb = load_workbook(filename = 'country_production_to_import.xlsx', data_only=True)
sheet = wb.active

# production year list
year_list = list()
for year in range(1994,2017):
	year_list.append(year)
print year_list

#read each row for the production and save to database
cell_range = sheet['A2': 'JS2']
for row in cell_range: # This is iterating through rows 1-7
    country_id = None
    country_name = None
    production_type = None
    production_list = list()
    counter = 0
    for cell in row: # This iterates through the columns(cells) in that row
    	if counter == 0:
    		country_id = int(cell.value)
        elif counter == 1 :
        	country_name = cell.value.strip()
        elif counter == 2:
        	production_type = cell.value.strip()
        else:
        	if cell.value is None:
        		production_list.append(0)
        	else:
        		production_list.append(int(cell.value))
        counter = counter + 1
print country_id, country_name, production_type, production_list
        	