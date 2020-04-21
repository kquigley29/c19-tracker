from covid import Covid
from bs4 import BeautifulSoup
import requests
import csv

from convert import pdf_to_csv, csv_to_dict


# --------------------------------
# Get country cases and death data
# --------------------------------

cov = Covid()


# use the covid package to get data on covid-19 (default source: John Hopkins University)
def get_cases_data():
    data = cov.get_data()
    return data

# filter country case deaths by country name
def filter_cases_by_country(country_name):
    data = get_cases_data()
    for entry in data:
        if country_name == entry.get('country'):
            return entry


# -------------------
# Get population data 
# -------------------

# get population data from Worldometer
def get_population_data():

    # get the webpage content
    wom_pop_response = requests.get('https://www.worldometers.info/world-population/population-by-country/')
    wom_pop = wom_pop_response.content
    soup = BeautifulSoup(wom_pop, 'html.parser')

    # get all the table rows
    table = soup.find('tbody')
    rows = table.find_all('tr')

    # get a list of lists of the row entries
    table_list = []
    for row in rows:
        row_list = []
        row_data = row.find_all('td')
        for entry in row_data:
            row_list.append(entry.text)
        table_list.append(row_list)

    # convert table list to dictionary to return
    table_data = []
    for row in table_list:
        row_dict = {}
        
        row_dict['rank'] = int(row[0]) 
        
        row_dict['country'] = row[1]
        
        try:
            row_dict['population'] = int(row[2].replace(',', ''))
        except ValueError:
            row_dict['population'] = None
        
        try:
            row_dict['yearly change'] = float(row[3].replace('%', ''))
        except ValueError:
            row_dict['yearly change'] = None
        
        try:
            row_dict['net change'] = int(row[4].replace(',', ''))
        except ValueError:
            row_dict['net change'] = None
        
        try:
            row_dict['density'] = int(row[5].replace(',', ''))
        except ValueError:
            row_dict['density'] = None
        
        try:
            row_dict['land area'] = int(row[6].replace(',', ''))
        except ValueError:
            row_dict['land area'] = None
        
        try:
            row_dict['migrants'] = int(row[7].replace(',', ''))
        except ValueError:
            row_dict['migrants'] = None
        
        try:
            row_dict['fertility rate'] = float(row[8])
        except ValueError:
            row_dict['fertility rate'] = None
        
        try:
            row_dict['median age'] = int(row[9])
        except ValueError:
            row_dict['median age'] = None
        
        try:
            row_dict['urban population %'] = float(row[10].replace('%', ''))
        except ValueError:
            row_dict['urban population %'] = None
        
        try:
            row_dict['world share %'] = float(row[11].replace('%', ''))
        except ValueError:
            row_dict['world share %'] = None

        table_data.append(row_dict)

    return table_data  


# filter country population data by country name
def filter_population_data(country_name):
    data = get_population_data()
    for entry in data:
        if country_name == entry.get('country'):
            return entry
        

# test functions
def find_country(country_name):
    data = get_population_data()
    for d in data:
        if d['country'] == country_name:
            return d

def ranks():
    data = get_population_data()
    r = []
    for d in data:
        r.append(d['rank'])
    return r
    

# to test the functions
if __name__ == '__main__':
    pass