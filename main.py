#!/usr/bin/python
import change

from flask import render_template, Flask, request, json
from googletrans import Translator
import requests
translator = Translator()
import requests
from bs4 import BeautifulSoup
from igramscraper.instagram import Instagram
from flask_cors import CORS
# from firebase import firebase
from datetime import date
from datetime import datetime

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
  return render_template("index.html")

@app.route('/india')
def getstats():
  retJSON = requests.get('https://api.rootnet.in/covid19-in/stats/latest')
  data = retJSON.json()
  return data

@app.route('/usa')
def getUSAStats():
  website_url = requests.get('https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_the_United_States').text
  soup = BeautifulSoup(website_url,'lxml')
  My_table = soup.find('table',{'class':'wikitable plainrowheaders sortable'})
  retJSON = {}
  data = []
  links = My_table.find_all('tr')

  for link in links:
      dataTag = link.find_all('td')
      headingTag = link.find_all('th')
      
      if(len(headingTag) == 2):
          state = headingTag[1].text.rstrip("\n")
          if(len(dataTag) == 5):
              cases = dataTag[0].text.rstrip("\n")
              deaths = dataTag[1].text.rstrip("\n")
              recovered = dataTag[2].text.rstrip("\n")
              region = {
                  "state": state,
                  "cases": cases,
                  "deaths": deaths,
                  "recovered": recovered
              }
              data.append(region)
  retJSON['data'] = data
  return retJSON

@app.route('/spain')
def getSPAINStats():
  website_url = requests.get('https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Spain').text
  soup = BeautifulSoup(website_url,'lxml')
  My_table = soup.find('table',{'class':'wikitable sortable'})
  retJSON = {}
  data = []
  links = My_table.find_all('tr')
  for link in links:
      dataTag = link.find_all('td')
      if(len(dataTag) == 9):
          state = dataTag[0].text.rstrip("\n").replace('(article)','')
          cases = dataTag[1].text.rstrip("\n")
          deaths = dataTag[4].text.rstrip("\n")
          recovered = dataTag[5].text.rstrip("\n")
          region = {
              "state": state,
              "cases": cases,
              "deaths": deaths,
              "recovered": recovered
          }
          data.append(region)
  retJSON['data'] = data
  return retJSON

@app.route('/italy')
def getITALYStats():
  website_url = requests.get('https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Italy').text
  soup = BeautifulSoup(website_url,'lxml')
  My_table = soup.find('table',{'class':'wikitable sortable'})
  retJSON = {}
  data = []
  links = My_table.find_all('tr')
  for link in links:
      dataTag = link.find_all('td')
      headingTag = link.find_all('th')
      if(len(headingTag) == 1):
        state = headingTag[0].text.rstrip("\n")
        if(state == 'Italy'):
          state = 'Total'
        if(len(dataTag) == 10):
              cases = dataTag[0].text.rstrip("\n")
              deaths = dataTag[1].text.rstrip("\n")
              recovered = dataTag[5].text.rstrip("\n")
              region = {
                  "state": state,
                  "cases": cases,
                  "deaths": deaths,
                  "recovered": recovered
              }
              data.append(region)
  retJSON['data'] = data
  return retJSON

    
if __name__ == '__main__':
  app.run(debug=True)
