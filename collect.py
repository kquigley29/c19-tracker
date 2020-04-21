from covid import Covid
from bs4 import BeautifulSoup
import requests
import csv

from convert import pdf_to_csv, csv_to_dict


# ------------------------------------------------
# Get country cases/death data and population data
# ------------------------------------------------
cov = Covid()


# use the covid package to get data on covid-19 (default source: Worldometer)
def get_cases_data():
    data = cov.get_data()
    return data

# filter country case deaths by country name
def filter_cases_by_country(country_name):
    data = get_cases_data()
    for entry in data:
        if country_name == entry.get('country'):
            return entry


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
            if entry.text != 'N/A':
                row_list.append(entry.text)
            else:
                row_list.append(None)
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
            row_dict['yearly change'] = float(row[3].replace('%', '')) / 100
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
            row_dict['urban population %'] = float(row[10].replace('%', '')) / 100
        except ValueError:
            row_dict['urban population %'] = None
        
        try:
            row_dict['world share %'] = float(row[11].replace('%', '')) / 100
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


# ------------------
# Get treatment data
# ------------------
def get_treatment_data():
    
    # get the webpage content
    milken_response = requests.get('https://milkeninstitute.org/covid-19-tracker')
    milken = milken_response.content
    soup = BeautifulSoup(milken, 'html.parser')

    # get all the links and find the link to the pdf
    data_links = soup.find_all('a')
    for link in data_links:
        if link.text == "VIEW COVID-19 TRACKER":
            pdf_url = link.attrs['href']

    # get the pdf doc and update treatment_data.pdf with it
    milken_pdf_response = requests.get(pdf_url)
    with open('treatment_data.pdf', 'wb') as doc:
        doc.write(milken_pdf_response.content)

    # convert the pdf into csv format
    pdf_to_csv('treatment_data.pdf')
        

# to test the functions
if __name__ == '__main__':
    get_population_data()
