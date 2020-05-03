import csv
import requests
import codecs
from datetime import datetime
from models import OwidData


def stringToFloat(str):
    b = 0
    try:
        b = int(float(str))
    except:
        b = 0
    finally:
        return b


def owid(thisSession):
    try:
        url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        response = requests.get(url)
        text = response.iter_lines()
        cr = csv.reader(codecs.iterdecode(text, 'utf-8'), delimiter=",")

        thisSession.query(OwidData).delete()

        first_row=next(cr)
        for row in cr:
            #print(row[2].split("-")[0])
            owidData= OwidData(**{
                'name': row[1],
                'date': datetime(int(row[2].split("-")[0]), int(row[2].split("-")[1]), int(row[2].split("-")[2])),
                'total_cases': stringToFloat(row[3]),
                'new_cases': stringToFloat(row[4]),
                'total_deaths': stringToFloat(row[5]),
                'new_deaths': stringToFloat(row[6]),
                'total_cases_per_million': stringToFloat(row[7]),
                'total_deaths_per_million': stringToFloat(row[9]),
                'total_tests': stringToFloat(row[11]),
                'new_tests': stringToFloat(row[12]),
                'total_tests_per_thousand': stringToFloat(row[13])
            })
            thisSession.add(owidData)
        thisSession.commit()

    except Exception as e:
        print(e)
        thisSession.rollback()
    finally:

        thisSession.close()
