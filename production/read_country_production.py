from openpyxl import load_workbook
wb = load_workbook(filename = 'country_production_to_import.xlsx')
sheet_ranges = wb['Sheet1']
print(sheet_ranges['D18'].value)