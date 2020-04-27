import csv
from models import MilkenData



def milken(thisSession):
    try:
        file = 'milken.csv'
        cr = csv.reader(file, delimiter=",")

        thisSession.query(MilkenData).delete()

        first_row=next(cr)
        for row in cr:
            #print(row[2].split("-")[0])
            milkenData= MilkenData(**{
                'treatment_or_vaccine': row[0],
                'catagory': row[1],
                'description': row[2],
                'stage': row[3],
                'next_steps': row[4],
                'clinical_trials': row[5],
                'developer': row[6],
                'funder': row[7],
                'results': row[8],
                'other_uses': row[9],
                'fda_approval': row[10]
            })
            thisSession.add(milkenData)
        thisSession.commit()
    
    except Exception as e:
        print(e)
        thisSession.rollback()
    finally:
        
        thisSession.close()
