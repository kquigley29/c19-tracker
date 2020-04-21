import flask
from flask import request, jsonify
from collect import get_cases_data, filter_cases_by_country, get_population_data,filter_population_data
from convert import dict_to_html

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# app.config["SQLALCHEMY_DATABASE_URI"] = True
# db = SQLAlchemy(app)

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


# -------------------------
# Accessing country data.
# -------------------------
@app.route('/api/v1/cases/all', methods=['GET'])
def cases_all():
    cases_message = '''<h1>Cases Data</h>'''
    cases_data = get_cases_data()

    # check for format param
    query_params = request.args
    format = query_params.get('format')
    if format:
        if format == 'json':
            return jsonify(cases_data)

        elif format == 'html':
            return dict_to_html(cases_data)
        
        elif format != 'json' and format != 'html':
            return "<h1>Error</h1><p>Format unavaliable</p>"
    
    # if no params is given, return as json
    else:
        return jsonify(cases_data)


@app.route('/api/v1/cases', methods=['GET'])
def cases_filter():
    query_params = request.args
    country = query_params.get('country')
    format = query_params.get('format')

    # get the requested country
    if country:
        filtered_cases_data = [filter_cases_by_country(country)]

    # display the data in the requested format
    if format:
        if format == 'json':
            return jsonify(filtered_cases_data)

        elif format == 'html':
            return dict_to_html(filtered_cases_data)
        
        elif format != 'json' and format != 'html':
            return "<h1>Error</h1><p>Format unavaliable</p>"
    
    # if no format is requested display in json
    else:
        return jsonify(filtered_cases_data)


@app.route('/api/v1/population/all', methods=['GET'])
def pop_all():
    pop_data = get_population_data()

    # check for format param
    query_params = request.args
    format = query_params.get('format')
    if format:
        if format == 'json':
            return jsonify(pop_data)

        elif format == 'html':
            return dict_to_html(pop_data)
        
        elif format != 'json' and format != 'html':
            return "<h1>Error</h1><p>Format unavaliable</p>"
    
    # if no params is given, return as json
    else:
        return jsonify(pop_data)


@app.route('/api/v1/population', methods=['GET'])
def pop_filter():
    query_params = request.args
    country = query_params.get('country')
    format = query_params.get('format')

    if country:
        filtered_pop_data = [filter_population_data(country)]

    # display the data in the requested format
    if format:
        if format == 'json':
            return jsonify(filtered_pop_data)

        elif format == 'html':
            return dict_to_html(filtered_pop_data)
        
        elif format != 'json' and format != 'html':
            return "<h1>Error</h1><p>Format unavaliable</p>"
    
    # if no format is requested display in json
    else:
        return jsonify(filtered_pop_data)
    

if __name__ == '__main__':
    app.run()
