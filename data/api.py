from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import OwidData, OxfordData, MilkenData, PopulationData
from models import Base
import json
import copy


app=Flask(__name__)
cors = CORS(app)
engine = create_engine("sqlite:////home/keane/visceraApi/data.db")
Base.metadata.create_all(engine)
app.config['DEBUG'] = True

# ---------
# Owid data
# ---------

# get latest data for a country
@app.route("/owid/current/<country>")
@cross_origin()
def countryData(country):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(OwidData).filter_by(name=country)
    session.close()

    # deep copy is done so that the object is not a reference to
    # the database so modifying it produces no changes in database
    r = copy.deepcopy(query[query.count()-1])

    # if there is no test data for this day, then traverse backwards
    # through the days and set the test data to the most recent one
    if(r.total_tests == 0):
        for i in range(query.count()-1, -1, -1):
            if(query[i].total_tests != 0):
                r.total_tests = query[i].total_tests
                r.total_tests_per_thousand = query[i].total_tests_per_thousand
                break

    return r.toJson()


# get latest data for all countries
@app.route("/owid/current/all")
@cross_origin()
def allCountries():
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(OwidData).all()

    length = len(query)
    r=[]
    for index, t in enumerate(query):
        if index != (length-1):
            if t.name == "World":

                continue
            if t.name != query[index+1].name:
                # this tests if the total_tests is 0, if so it looks at previous
                # days until the tests is not 0 and assigns that value
                temp = copy.deepcopy(t)
                if(t.total_tests == 0):
                    i = index-1
                    while(query[i].name == t.name):
                        if(query[i].total_tests != 0):
                            temp.total_tests = query[i].total_tests
                            temp.total_tests_per_thousand = query[i].total_tests_per_thousand
                            break
                        i = i-1
                if(t.total_cases == 0):
                    i = index-1
                    while(query[i].name == t.name):
                        if(query[i].total_cases != 0):
                            temp.total_cases = query[i].total_cases
                            temp.total_cases_per_million = query[i].total_cases_per_million
                            break
                        i = i-1
                if(t.total_deaths == 0):
                    i = index-1
                    while(query[i].name == t.name):
                        if(query[i].total_deaths != 0):
                            temp.total_deaths = query[i].total_deaths
                            temp.total_deaths_per_million = query[i].total_deaths_per_million
                            break
                        i = i-1

                r.append(temp.toJson())

        else:
            temp = copy.deepcopy(t)
            if(t.total_tests == 0):
                i = index-1
                while(query[i].name == t.name):
                    if(query[i].total_tests != 0):
                        temp.total_tests = query[i].total_tests
                        temp.total_tests_per_thousand = query[i].total_tests
                        break
                    i = i-1
            r.append(t.toJson())
        session.close()

    return jsonify(r)


# get the historical data for a country
@app.route("/owid/history/<country>")
@cross_origin()
def countryHistoryData(country):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(OwidData).filter_by(name=country)
    session.close()
    r = []
    for t in query:
        r.append(t.toJson())
    
    return jsonify(r)

#get past two weeks for every country
@app.route("/owid/history/allRecent")
@cross_origin()
def allHistoryData():
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(OwidData).all()
    session.close()
    length = len(query)
    temp = []
    r = {}
    for index, t in enumerate(query):
        if index != (length-1):
            if t.name != query[index+1].name:
                numDays = 13
                name = t.name
                while(numDays>=0):
                    if query[index-numDays].name != name:
                        numDays=numDays-1
                        continue
                    temp.append(query[index-numDays].toJson())
                    numDays = numDays-1
                r[name] = copy.deepcopy(temp)
                temp = []
        else:

            numDays = 13
            name = t.name
            while(numDays>=0):
                temp.append(query[index-numDays].toJson())
                numDays = numDays-1
            r[name] = copy.deepcopy(temp)
            temp = []

    return jsonify(r)


# ----------
# Oxford data
# ----------

# get latest data for a country
@app.route("/oxford/current/<country>")
@cross_origin()
def oxfordCurrentIndividual(country):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(OxfordData).filter_by(name=country)
    session.close()

    # deep copy is done so that the object is not a reference to
    # the database so modifying it produces no changes in database
    r = copy.deepcopy(query[query.count()-1])

    return r.toJson()

# get latest data for all countries
@app.route("/oxford/current/all")
@cross_origin()
def oxfordCurrentAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(OxfordData).all()
    length = len(query)
    r=[]
    for index, t in enumerate(query):
        if index != (length-1):
            if t.name != query[index + 1].name:
                r.append(t.toJson())
        else:
            r.append(t.toJson())

    return jsonify(r)


# get the historical data for a country
@app.route("/oxford/history/<country>")
@cross_origin()
def oxfordHistoryIndividual(country):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(OxfordData).filter_by(name=country)
    session.close()
    r = []
    for t in query:
        r.append(t.toJson())

    return jsonify(r)


# -----------
# Milken Data
# -----------

# get all data on treatments and vaccines
@app.route("/milken/all")
@cross_origin()
def milkenAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(MilkenData).all()
    session.close()
    
    r = []
    for t in query:
        # deep copy is done so that the object is not a reference to 
        # the database so modifying it produces no changes in database
        s = copy.deepcopy(t)
        r.append(s.toJson())

    return jsonify(r)


# get data on treatments only
@app.route("/milken/treatments")
@cross_origin()
def milkenTreatments():
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(MilkenData).filter_by(treatment_or_vaccine='Treatment')
    session.close()
    
    r = []
    for t in query:
        # deep copy is done so that the object is not a reference to 
        # the database so modifying it produces no changes in database
        s = copy.deepcopy(t)
        r.append(s.toJson())

    return jsonify(r)


# get data on vaccines only
@app.route("/milken/vaccines")
@cross_origin()
def milkenVaccines():
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(MilkenData).filter_by(treatment_or_vaccine='Vaccine')
    session.close()
    
    r = []
    for t in query:
        # deep copy is done so that the object is not a reference to 
        # the database so modifying it produces no changes in database
        s = copy.deepcopy(t)
        r.append(s.toJson())

    return jsonify(r)


# ---------------------------
# Worldometer Population Data
# ---------------------------

@app.route("/worldometer/population/all")
@cross_origin()
def populationAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(PopulationData).all()
    session.close()

    r = []
    for t in query:
        # deep copy is done so that the object is not a reference to 
        # the database so modifying it produces no changes in database
        s = copy.deepcopy(t)
        r.append(s.toJson())
    
    return jsonify(r)


@app.route('/worldometer/population/<country>')
@cross_origin()
def populationIndividual(country):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(PopulationData).filter_by(country=country)
    session.close()
    
    # deep copy is done so that the object is not a reference to 
    # the database so modifying it produces no changes in database
    r = copy.deepcopy(query[-1])

    return r.toJson()


if(__name__ == '__main__'):
    app.run()