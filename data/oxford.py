import csv
import requests
import codecs
from datetime import datetime
from data.models import OxfordData


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
                'date': datetime(int(row[4][0:4]), int(row[4][4:6]), int(row[4][6:])),
                'school_closing': stringToFloat(row[5]),
                'workplace_closing': stringToFloat(row[7]),
                'cancel_public_events': stringToFloat(row[9]),
                'gatherings_restrictions': stringToFloat(row[11]),
                'close_public_transport': stringToFloat(row[13]),
                'stay_at_home_requirements': stringToFloat(row[15]),
                'internal_movement_restrictions': stringToFloat(row[17]),
                'international_travel_controls': stringToFloat(row[19]),
                'income_support': stringToFloat(row[20]),
                'debt_relief': stringToFloat(row[22]),
                'fiscal_measures': stringToFloat(row[23]),
                'international_support': stringToFloat(row[24]),
                'public_information_campaigns': stringToFloat(row[25]),
                'testing_policy': stringToFloat(row[27]),
                'contact_tracing': stringToFloat(row[28]),
                'emergency_investment_in_healthcare': stringToFloat(row[29]),
                'investment_in_vaccines': stringToFloat(row[30]),
                'confirmed_cases': stringToFloat(row[32]),
                'confirmed_deaths': stringToFloat(row[33]),
                'stringency_index': stringToFloat(row[34]),
                'stringency_index_for_display': stringToFloat(row[35]),
                'legacy_stringency_index': stringToFloat(row[36]),
                'legacy_stringency_index_for_display': stringToFloat(row[37])
            })

            thisSession.add(oxfordData)
        thisSession.commit()

    except Exception as e:
        print(e, "[oxford]")
        thisSession.rollback()

    finally:
        thisSession.close()
