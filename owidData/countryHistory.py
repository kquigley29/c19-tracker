import csv
import requests
import codecs
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Column, Integer, Float, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Country_Data
from models import Base


def stringToFloat(str):
    b = 0
    try:
        b = int(float(str))
    except:
        b = 0
    finally:
        return b


if __name__ == '__main__':
    engine = create_engine("sqlite:///countryHistories.db")

    Base.metadata.create_all(engine)

    if not database_exists(engine.url):
        create_database(engine.url)

    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        response = requests.get(url)
        text = response.iter_lines()
        cr = csv.reader(codecs.iterdecode(text, 'utf-8'), delimiter=",")

        session.query(Country_Data).delete()

        first_row=next(cr)
        for row in cr:
            #print(row[2].split("-")[0])
            countryData= Country_Data(**{
                'name': row[1],
                'date': datetime(int(row[2].split("-")[0]), int(row[2].split("-")[1]), int(row[2].split("-")[2])),
                'total_cases': stringToFloat(row[3]),
                'total_deaths': stringToFloat(row[5]),
                'total_cases_per_million': stringToFloat(row[7]),
                'total_deaths_per_million': stringToFloat(row[9]),
                'total_tests': stringToFloat(row[11]),
                'total_tests_per_thousand': stringToFloat(row[13])
            })
            session.add(countryData)
        session.commit()
    
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        
        session.close()
