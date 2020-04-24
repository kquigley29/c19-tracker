from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Column, Integer, Float, Date, Text
from sqlalchemy.orm import sessionmaker
from models import OxfordData
from models import Base
import copy


app=Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True
engine = create_engine("sqlite:///countryData.db")
Base.metadata.create_all(engine)

#Get latest data for a country
@app.route("/current/<country>")
@cross_origin()
def currentIndividual(country):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(OxfordData).filter_by(name=country)
    session.close()
    
    #deep copy is done so that the object is not a reference to the database so modifying it produces no changes in database
    r = copy.deepcopy(query[query.count()-1])

    return (r.toJson())

#get latest data for all countries
@app.route("/current/all")
@cross_origin()
def currentAll():
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


#get the historical data for a country
@app.route("/history/<country>")
@cross_origin()
def historyIndividual(country):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(OxfordData).filter_by(name=country)
    session.close()
    r = []
    for t in query:
        r.append(t.toJson())
    return (jsonify(r))


app.run()
