from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Column, Integer, Float, Date, Text
from sqlalchemy.orm import sessionmaker
from models import Country_Data
from models import Base
import copy
app=Flask(__name__)
cors = CORS(app)
engine = create_engine("sqlite:///countryHistories.db")
Base.metadata.create_all(engine)

#Get latest data for a country
@app.route("/<country>")
@cross_origin()
def countryData(country):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Country_Data).filter_by(name=country)
    session.close()
    
    #deep copy is done so that the object is not a reference to the database so modifying it produces no changes in database
    r = copy.deepcopy(query[query.count()-1])

    #if there is no test data for this day, then traverse backwards through the days and set the test data to the most recent one
    if(r.total_tests == 0):              
        for i in range(query.count()-1, -1, -1):          
            if(query[i].total_tests != 0):
                r.total_tests = query[i].total_tests
                r.total_tests_per_thousand = query[i].total_tests_per_thousand
                break
    return (r.toJson())

#get latest data for all countries
@app.route("/all")
@cross_origin()
def allCountries():
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Country_Data).all()
    length = len(query)
    r=[]
    for index, t in enumerate(query):
        if index != (length-1):
            if t.name != query[index+1].name:
                #this tests if the total_tests is 0, if so it looks at previous days until the tests is not 0 and assigns that value
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
    return (jsonify(r))

#get the historical data for a country
@app.route("/history/<country>")
@cross_origin()
def countryHistoryData(country):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Country_Data).filter_by(name=country)
    session.close()
    r = []
    for t in query:
        r.append(t.toJson())
    return (jsonify(r))