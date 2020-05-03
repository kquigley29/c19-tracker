from os import getcwd, system
from csv import reader
from requests import get
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from models import MilkenData


def getCsv():
    # get the url for the google sheet from Milken's main tracker page
    milkenUrl = 'https://milkeninstitute.org/covid-19-tracker'
    response = get(milkenUrl)
    milkenTracker = response.content
    page = BeautifulSoup(milkenTracker, 'html.parser')
    csvUrl = page.find('a', href=True, text='VIEW COVID-19 TRACKER')['href']

    # set the optionsand preferences for Firefox with selenium
    options = Options()
    options.headless = True
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', getcwd())                         # downloads to the current directory
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', ('text/csv'))   # no pop up window when downloading csv files
    # profile.set_preference('browser.download.dir', '~/c19-tracker/data')            

    # find and download the csv version of the google sheet
    driver = webdriver.Firefox(firefox_profile=profile, options=options)
    driver.get(csvUrl)
    fileMenu = driver.find_element_by_xpath("//div[@id='docs-file-menu']")
    fileMenu.click()
    downloadMenu = driver.find_element_by_xpath("//span[@aria-label='Download d']")
    downloadMenu.click()
    csvDownload = driver.find_element_by_xpath("//span[@aria-label='Comma-separated values (.csv, current sheet) c']")
    csvDownload.click()

    # rename the csv
    system("rm milken.csv")
    system("mv 'COVID-19 Treatment and Vaccine Tracker - Treatments and Vaccines.csv' milken.csv")


def milken(thisSession):
    # retrieve the csv file to insert into the df
    getCsv()

    try:
        file = 'milken.csv'
        with open(file) as milken_csv:
            cr = csv.reader(milken_csv, delimiter=",")

            thisSession.query(MilkenData).delete()

            first_row=next(cr)
            for row in cr:
                milkenData= MilkenData(**{
                    'treatment_or_vaccine': row[2].replace('*', ''),
                    'catagory': row[3].replace('*', ''),
                    'description': row[4].replace('*', ''),
                    'stage': row[5].replace('*', ''),
                    'next_steps': row[6].replace('*', ''),
                    'clinical_trials': row[7].replace('*', ''),
                    'developer': row[8].replace('*', ''),
                    'funder': row[9].replace('*', ''),
                    'results': row[10].replace('*', ''),
                    'other_uses': row[11].replace('*', ''),
                    'fda_approval': row[12].replace('*', '')
                })
                thisSession.add(milkenData)
            thisSession.commit()
        
    except Exception as e:
        print(e)
        thisSession.rollback()
    finally:
        
        thisSession.close()
