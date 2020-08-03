import csv
import requests
import codecs
from datetime import datetime
from models import OxfordData


def stringToFloat(str):
    b = 0
    try:
        b = int(float(str))
    except:
        b = 0
    finally:
        return b

def oxford(thisSession):
    try:
        url = "https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv"
        response = requests.get(url)
        text = response.iter_lines()
        cr = csv.reader(codecs.iterdecode(text, 'utf-8'), delimiter=",")

        thisSession.query(OxfordData).delete()

        first_row=next(cr)
        for row in cr:
            oxfordData= OxfordData(**{
                'name': row[0],
                'date': datetime(int(row[2][0:4]), int(row[2][4:6]), int(row[2][6:])),
                'school_closing': stringToFloat(row[3]),
                'workplace_closing': stringToFloat(row[5]),
                'cancel_public_events': stringToFloat(row[7]),
                'gatherings_restrictions': stringToFloat(row[9]),
                'close_public_transport': stringToFloat(row[11]),
                'stay_at_home_requirements': stringToFloat(row[13]),
                'internal_movement_restrictions': stringToFloat(row[15]),
                'international_travel_controls': stringToFloat(row[17]),
                'income_support': stringToFloat(row[18]),
                'debt_relief': stringToFloat(row[20]),
                'fiscal_measures': stringToFloat(row[21]),
                'international_support': stringToFloat(row[22]),
                'public_information_campaigns': stringToFloat(row[23]),
                'testing_policy': stringToFloat(row[25]),
                'contact_tracing': stringToFloat(row[26]),
                'emergency_investment_in_healthcare': stringToFloat(row[27]),
                'investment_in_vaccines': stringToFloat(row[28]),
                'confirmed_cases': stringToFloat(row[30]),
                'confirmed_deaths': stringToFloat(row[31]),
                'stringency_index': stringToFloat(row[32]),
                'stringency_index_for_display': stringToFloat(row[33]),
                'legacy_stringency_index': stringToFloat(row[34]),
                'legacy_stringency_index_for_display': stringToFloat(row[35])
            })

            thisSession.add(oxfordData)
        thisSession.commit()

    except Exception as e:
        print(e, "[oxford]")
        thisSession.rollback()

    finally:
        thisSession.close()
