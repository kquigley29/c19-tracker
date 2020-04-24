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
        url = "https://ocgptweb.azurewebsites.net/CSVDownload"
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
                'workplace_closing': stringToFloat(row[6]),
                'cancel_public_events': stringToFloat(row[9]),
                'close_public_transport': stringToFloat(row[12]),
                'public_information_campaigns': stringToFloat(row[15]),
                'internal_movement_restrictions': stringToFloat(row[18]),
                'international_travel_controls': stringToFloat(row[21]),
                'fiscal_measures': stringToFloat(row[23]),
                'monetary_measures': stringToFloat(row[25]),
                'emergency_investment_in_healthcare': stringToFloat(row[27]),
                'investment_in_vaccines': stringToFloat(row[29]),
                'testing_framework': stringToFloat(row[31]),
                'contact_tracing': stringToFloat(row[33]),
                'stringency_index': stringToFloat(row[37]),
                'stringency_index_for_display': stringToFloat(row[38])
            })

            thisSession.add(oxfordData)
        thisSession.commit()
    
    except Exception as e:
        print(e)
        thisSession.rollback()

    finally:
        thisSession.close()
