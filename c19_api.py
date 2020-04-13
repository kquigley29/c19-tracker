import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d


@app.route('/', methods=['GET'])
def home():
    home_page_message = '''<h1>COVID-19 Treatment Tracker API</h1>
                               <p>An API for tracking the development of cures and prevention medication.</p>'''
    return home_page_message

@app.route('/api/v1/treatments/all', methods=['GET'])
def api_all():
    connection_ = sqlite3.connect('treatments.db')
    connection_.row_factory = dict_factory
    cursor_ = connection_.cursor()
    all_treatments = cursor_.execute('SELECT * FROM treatments;').fetchall()

    return jsonify(all_treatments)


@app.errorhandler(404)
def page_not_found():
    error_404_message = '''<h1>404</h1>
                               <p>Resource not found.</p>'''
    return error_404_message, 404


@app.route('/api/v1/treatments', methods=['GET'])
def api_filter():
    query_params = request.args

    id = query_params.get('id')
    name = query_params.get('name')
    stage = query_params.get('stage')
    colaborators = query_params.get('colaborators')

    query = "SELECT * FROM treatments WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if name:
        query += ' name=? AND'
        to_filter.append(name)
    if stage:
        query += ' stage=? AND'
        to_filter.append(stage)
    if colaborators:
        query += ' colaborators=? AND'
        to_filter.append(colaborators)
    if not (id or name or stage or colaborators):
        return error_404_message()

    query = query[:-4] + ';'

    connection_ = sqlite3.connect('treatments.db')
    connection_.row_factory = dict_factory
    cursor_ = connection_.cursor()

    results = cursor_.execute(query, to_filter).fetchall()

    return jsonify(results)


app.run()