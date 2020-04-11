from flask import render_template, Flask, request, json
from googletrans import Translator
import requests
translator = Translator()
import requests
from bs4 import BeautifulSoup
from igramscraper.instagram import Instagram

app = Flask(__name__)

langs = ['gu','bn','hi','kn','ta','te','en']
@app.route('/translate', methods=['POST', 'GET']) 
def translate():
    if request.method == 'POST':
        text = request.form['text']
        captions = {}
        for lan in langs:
          trans = []
          for word in text.split(' '):
            t = translator.translate(word, dest=lan)
            trans.append(t.text)
          translated = ' '.join(trans)
          captions[lan] = translated
        return render_template('trans.html', captions=captions) 
    else:
        return render_template('trans.html')

@app.route('/')
def home():
  return render_template("index.html")

@app.route('/stats')
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
      if(len(dataTag) == 6):
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
        if(len(dataTag) == 9):
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

@app.route('/covidai')
def getigStats():
  instagram = Instagram()
  data = { 'account': {}}
  account = instagram.get_account('covid.ai_tamil')
  data['account']['id'] = account.identifier
  data['account']['username'] = account.username
  data['account']['Full name'] = account.full_name
  data['account']['Biography'] = account.biography
  data['account']['Profile pic url'] = account.get_profile_picture_url()
  data['account']['Number of published posts'] = account.media_count
  data['account']['Number of followers'] = account.followed_by_count
  data['account']['Number of follows'] = account.follows_count

  # total_likes = 0
  # total_comments = 0
  # coms = []
  # medias = instagram.get_medias("covid.ai", 1000)
  # for x in medias:
  #     total_likes += x.likes_count
  #     total_comments += x.comments_count
  # data['comments'] = coms
  # data['total_likes'] = total_likes
  # data['total_comments'] = total_comments
  return data
  
@app.route('/coms')
def getcomments():
  instagram = Instagram()
  data = {}
  coms = []
  medias = instagram.get_medias("covid.ai_tamil", 1000)
  for x in medias:
    comments = instagram.get_media_comments_by_id(x.identifier, 10000)
    for comment in comments['comments']:
        coms.append(comment.text)
  data['comments'] = coms
  return data


if __name__ == '__main__':
  app.run(host='0.0.0.0',port='8001', debug=True)
