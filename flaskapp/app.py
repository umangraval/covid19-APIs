from flask import render_template, Flask, request, json
from googletrans import Translator
import requests
translator = Translator()
import requests
from bs4 import BeautifulSoup
from igramscraper.instagram import Instagram
from flask_cors import CORS
from firebase import firebase
from datetime import date
from datetime import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True)


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

  today = date.today().strftime("%Y-%m-%d")
  firebse = firebase.FirebaseApplication('https://covidai-1dd78.firebaseio.com/', None)
  previous = firebse.get('https://covidai-1dd78.firebaseio.com/covidai-1dd78/followcount/covidaitamil/', '')
  da = previous.get(today, '')
  if(da):
    diff = account.followed_by_count - previous[today]
    data['account']['diff'] = diff
  else:
    result = firebse.put('https://covidai-1dd78.firebaseio.com/covidai-1dd78/followcount/covidaitamil/', today, account.followed_by_count)
    diff = account.followed_by_count - previous[today]
    print('update')
    data['account']['diff'] = diff
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

@app.route('/likesncoms')
def getlikesncoms():
  instagram = Instagram()
  data = {'like_timeline': {},
  'comment_timeline': {}}
  total_likes = 0
  total_comments = 0
  firebse = firebase.FirebaseApplication('https://covidai-1dd78.firebaseio.com/', None)
  previous = firebse.get('https://covidai-1dd78.firebaseio.com/covidai-1dd78/like_timeline/', '')
  medias = instagram.get_medias("covid.ai_tamil", 1000)
  flag = 0
  for x in medias:
    timestamp = x.created_time
    dh_object = datetime.fromtimestamp(timestamp).strftime("%H")
    # dd_object = date.fromtimestamp(timestamp)
    if(flag == 0):
      data['like_timeline'][dh_object] = x.likes_count
      data['comment_timeline'][dh_object] = x.comments_count
    else:
      data['like_timeline'][dh_object] += x.likes_count
      data['comment_timeline'][dh_object] += x.comments_count  
    #   result = firebse.put('https://covidai-1dd78.firebaseio.com/covidai-1dd78/followcount/covidaitamil/', today, account.followed_by_count)
    total_likes += x.likes_count
    total_comments += x.comments_count
  data['total_likes'] = total_likes
  data['total_comments'] = total_comments
  return data

@app.route('/latest')
def getlatest():
  data = {}
  instagram = Instagram()
  medias = instagram.get_medias("covid.ai_tamil", 1)
  for x in medias:
    data['created_time'] = x.created_time
    data['caption'] = x.caption
    data['likes_count'] = x.likes_count
    data['comments_count'] = x.comments_count
    data['image_high_resolution_url'] = x.image_high_resolution_url
    data['link'] = x.link
  return data


if __name__ == '__main__':
  app.run(host='0.0.0.0',port='8001', debug=True)
