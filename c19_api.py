import flask
import sqlite3
from flask import request, jsonify
from collect import get_cases_data, filter_cases_by_country, get_population_data,filter_population_data
from convert import dict_to_html


app = flask.Flask(__name__)
app.config["DEBUG"] = True


def dict_factory(cursor, row):
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d


@app.errorhandler(404)
def page_not_found(error):
    error_404_message = '''<h1>404</h1>
                               <p>Resource not found.</p>'''
    return error_404_message


@app.route('/', methods=['GET'])
def home():
    home_page_message = '''<h1>COVID-19 Tracker API</h1>
                               <p>An API for tracking the corona-19 situation.</p>'''
    home_page_links = '''<ul>
                             <li><a href=./api/v1/cases/all>cases</a></li>
                             <li><a href=./api/v1/population/all>population</a></li>
                         </ul>'''
    
    return home_page_message + home_page_links


# ----------------------
# Accessing country data
# ----------------------

@app.route('/api/v1/cases/all', methods=['GET'])
def cases_all():
    cases_message = '''<h1>Cases Data</h>'''
    cases_data = get_cases_data()

    return jsonify(cases_data)


@app.route('/api/v1/cases', methods=['GET'])
def cases_filter():
    query_params = request.args
    country = query_params.get('country')

    return jsonify(filtered_cases_data)


@app.route('/api/v1/population/all', methods=['GET'])
def pop_all():
    pop_data = get_population_data()

    return jsonify(pop_data)


@app.route('/api/v1/population', methods=['GET'])
def pop_filter():
    query_params = request.args
    country = query_params.get('country')

    if country:
        filtered_pop_data = [filter_population_data(country)]

        return jsonify(filtered_pop_data)
    

# ----------------------------
# Display data in the datebase
# ----------------------------

# @app.route('/api/v1/c19data/all', methods=['GET'])
# def data_all():
#     conn = sqlite3.connect('covid.db')
#     conn.row_factory = dict_factory
#     cur = conn.cursor()
#     all_data = cur.execute('SELECT * FROM all_data;').fetchall()

#     return jsonify(all_data)


@app.route('/api/v1/c19data/current/all', methods=['GET'])
def current_data_all():
    conn = sqlite3.connect('covid.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    query_params = request.args
    country = query_params.get('country')
    to_filter = []

    all_data = cur.execute('SELECT * FROM current_data;').fetchall()
    return jsonify(all_data)


@app.route('/api/v1/c19data/current', methods=['GET'])
def current_data_filter():
    conn = sqlite3.connect('covid.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    query_params = request.args

    country = query_params.get('country')
    iso_code = query_params.get('iso_code')
    to_filter = []

    query = 'SELECT * FROM current_data WHERE'
    

    if country:
        query += ' location=? AND'
        to_filter.append(country)
    if iso_code:
        query += ' iso_code=? AND'
        to_filter.append(iso_code)

    query = query[:-4] + ';'
        
    filtered_data = cur.execute(query, to_filter).fetchall()

    return jsonify(filtered_data)


if __name__ == '__main__':
    app.run()
