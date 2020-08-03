import csv
import requests
import codecs
from datetime import datetime
from models import OwidData


def stringToFloat(in_str):
    b = 0
    try:
        b = int(float(in_str))
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

        first_row = next(cr)
        for row in cr:
            # print(row[2].split("-")[0])
            owidData = OwidData(**{
                'name': row[2],
                'date': datetime(int(row[3].split("-")[0]), int(row[3].split("-")[1]), int(row[3].split("-")[2])),
                'total_cases': stringToFloat(row[4]),
                'new_cases': stringToFloat(row[5]),
                'total_deaths': stringToFloat(row[6]),
                'new_deaths': stringToFloat(row[7]),
                'total_cases_per_million': stringToFloat(row[8]),
                'total_deaths_per_million': stringToFloat(row[10]),
                'total_tests': stringToFloat(row[13]),
                'total_tests_per_thousand': stringToFloat(row[14])
            })
            thisSession.add(owidData)
        thisSession.commit()

    except Exception as e:
        print(e, "[owid]")
        thisSession.rollback()
    finally:

        thisSession.close()
