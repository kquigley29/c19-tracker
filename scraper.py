from covid import Covid
from bs4 import BeautifulSoup
import csv
import sqlite3
from converter import pdf_to_csv, csv_to_dict


# ----------------------------
# Get country cases/death data
# ----------------------------
cov = Covid()


def get_data():
    data = cov.get_data()
    return data


def filter_by_country(country_name):
    data = get_data()
    for entry in data:
        if country_name == entry.get('country'):
            return entry


# ------------------
# Get treatment data
# ------------------

