from covid import Covid
from convert import csv_to_dict


# --------------------------------
# Get country cases and death data
# --------------------------------

cov = Covid()


# use the covid package to get data on covid-19 (default source: John Hopkins University)
def get_cases_data():
    data = cov.get_data()
    return data


# filter country case deaths by country name
def filter_cases_by_country(country_name):
    data = get_cases_data()
    for entry in data:
        if country_name == entry.get('country'):
            return entry
