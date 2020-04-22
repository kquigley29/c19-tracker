from flask import Flask
from flask import jsonify
from flask import request
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Column, Integer, Float, Date, Text
from sqlalchemy.orm import sessionmaker
from models import Country_Data
from models import Base

app=Flask(__name__)

engine = create_engine("sqlite:///countryHistories.db")
Base.metadata.create_all(engine)

@app.route("/<country>")
def countryData(country):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Country_Data).filter_by(name=country)
    session.close()
    r = query[query.count()-1]
    return (r.toJson())
@app.route("/all")
def allCountries():
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Country_Data).all()
    length = len(query)
    r=[]
    for index, t in enumerate(query):
        if index != (length-1):
            if t.name != query[index+1].name:
                r.append(t.toJson())
        else:
            r.append(t.toJson())
    return (jsonify(r))
@app.route("/history/<country>")
def countryHistoryData(country):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Country_Data).filter_by(name=country)
    session.close()
    r = []
    for t in query:
        r.append(t.toJson())
    return (jsonify(r))