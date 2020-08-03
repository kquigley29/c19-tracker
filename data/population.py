import requests
import codecs
from models import PopulationData
from bs4 import BeautifulSoup


def stringToFloat(str):
    b = 0
    try:
        b = int(float(str))
    except:
        b = 0
    finally:
        return b


def getTable():
    url = "https://www.worldometers.info/world-population/population-by-country/"
    response = requests.get(url)
    worldometers_population = response.content
    page = BeautifulSoup(worldometers_population, 'html.parser')
    table = page.find('tbody')
    rows = table.find_all('tr')
    
    table_list = []
    for row in rows:
        row_list = []
        row_data = row.find_all('td')
        for entry in row_data:
            row_list.append(entry.text)
        table_list.append(row_list)

    return table_list


def population(thisSession):
    try:
        table = getTable()

        thisSession.query(PopulationData).delete()

        for row in table:
            row_dict = {}

            try:
                row_dict['rank'] = int(row[0].replace(',', ''))
            except ValueError:
                row_dict['rank'] = None
        
            row_dict['country'] = row[1]
        
            try:
                row_dict['population'] = int(row[2].replace(',', ''))
            except ValueError:
                row_dict['population'] = None
            
            try:
                row_dict['yearly_change'] = float(row[3].replace('%', ''))
            except ValueError:
                row_dict['yearly_change'] = None
            
            try:
                row_dict['net_change'] = int(row[4].replace(',', ''))
            except ValueError:
                row_dict['net_change'] = None
            
            try:
                row_dict['density'] = int(row[5].replace(',', ''))
            except ValueError:
                row_dict['density'] = None
            
            try:
                row_dict['land_area'] = int(row[6].replace(',', ''))
            except ValueError:
                row_dict['land_area'] = None
            
            try:
                row_dict['migrants'] = int(row[7].replace(',', ''))
            except ValueError:
                row_dict['migrants'] = None
            
            try:
                row_dict['fertility_rate'] = float(row[8])
            except ValueError:
                row_dict['fertility_rate'] = None
            
            try:
                row_dict['median_age'] = int(row[9])
            except ValueError:
                row_dict['median_age'] = None
            
            try:
                row_dict['urban_population'] = float(row[10].replace('%', ''))
            except ValueError:
                row_dict['urban_population'] = None
            
            try:
                row_dict['world_share'] = float(row[11].replace('%', ''))
            except ValueError:
                row_dict['world_share'] = None

            populationData= PopulationData(**row_dict)

            thisSession.add(populationData)
        thisSession.commit()
    
    except Exception as e:
        print(e, "[population]")
        thisSession.rollback()

    finally:
        thisSession.close()
