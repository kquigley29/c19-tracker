from covid import Covid
from bs4 import BeautifulSoup
import requests
import csv

from converter import pdf_to_csv, csv_to_dict


# ----------------------------
# Get country cases/death data
# ----------------------------
cov = Covid()


def get_cases_data():
    data = cov.get_data()
    return data


def filter_cases_by_country(country_name):
    data = get_cases_data()
    for entry in data:
        if country_name == entry.get('country'):
            return entry


# ------------------
# Get treatment data
# ------------------
def get_treatment_data():
    
    # get webpage content
    milken_response = requests.get("https://milkeninstitute.org/covid-19-tracker")
    milken = milken_response.content
    soup = BeautifulSoup(milken, 'html.parser')

    # get all the links and find the link to the pdf
    data_links = soup.find_all('a')
    for link in data_links:
        if link.text == "VIEW COVID-19 TRACKER":
            pdf_url = link.attrs['href']

    # get the pdf doc and update treatment_data.pdf with it
    milken_pdf_response = requests.get(pdf_url)
    with open('treatment_data.pdf', 'wb') as doc:
        doc.write(milken_pdf_response.content)

    # convert the pdf into csv format
    pdf_to_csv('treatment_data.pdf')
        

if __name__ == '__main__':
    get_cases_data()
    get_treatment_data()
