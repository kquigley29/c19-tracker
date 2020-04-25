from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import OwidData, OxfordData
from models import Base
import json
import copy


app=Flask(__name__)
cors = CORS(app)
engine = create_engine("sqlite:///data.db")
Base.metadata.create_all(engine)


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
    return (r.toJson())


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
            if t.name != query[index+1].name:
                # this tests if the total_tests is 0, if so it looks at previous 
                # days until the tests is not 0 and assigns that value
                temp = copy.deepcopy(t)
                if(t.total_tests == 0):              
                    i = index-1
                    while(query[i].name == t.name):
                        if(query[i].total_tests != 0):
                            temp.total_tests = query[i].total_tests
                            temp.total_tests_per_thousand = query[i].total_tests
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
    return (jsonify(r))


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
    return (jsonify(r))

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
    return (jsonify(r))


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

    return (r.toJson())

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

    return (jsonify(r))


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
    return (jsonify(r))


if(__name__ == '__main__'):
    app.run()
