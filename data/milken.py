import csv
from models import MilkenData



def milken(thisSession):
    try:
        file = 'milken.csv'
        with open(file) as milken_csv:
            cr = csv.reader(milken_csv, delimiter=",")

            thisSession.query(MilkenData).delete()

            first_row=next(cr)
            for row in cr:
                milkenData= MilkenData(**{
                    'treatment_or_vaccine': row[2].replace('*', ''),
                    'catagory': row[3].replace('*', ''),
                    'description': row[4].replace('*', ''),
                    'stage': row[5].replace('*', ''),
                    'next_steps': row[6].replace('*', ''),
                    'clinical_trials': row[7].replace('*', ''),
                    'developer': row[8].replace('*', ''),
                    'funder': row[9].replace('*', ''),
                    'results': row[10].replace('*', ''),
                    'other_uses': row[11].replace('*', ''),
                    'fda_approval': row[12].replace('*', '')
                })
                thisSession.add(milkenData)
            thisSession.commit()
        
    except Exception as e:
        print(e)
        thisSession.rollback()
    finally:
        
        thisSession.close()
