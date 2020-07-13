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
from firebase import firebase
from datetime import date
from datetime import datetime

app = Flask(__name__)
CORS(app)

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

@app.route('/<username>')
def getigStats(username):
  instagram = Instagram()
  data = { 'account': {}}
  account = instagram.get_account(username)
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
  previous = firebse.get('https://covidai-1dd78.firebaseio.com/covidai-1dd78/followcount/', '')
  keys = previous.keys()
  print(keys)
  newEntry = 0
  for key in keys:
    if(username == key):
      newEntry = 1
      for sna in previous[key].keys():
        stamp = sna
      print(stamp)
      Dataurl = 'https://covidai-1dd78.firebaseio.com/covidai-1dd78/followcount/'+username+'/'
      flag = 0
      previous = firebse.get(Dataurl+stamp, '')
      print(previous)
      da = previous[-1].get(today, '')
      print(da)
      if(da):
        diff = account.followed_by_count - previous[-1][today]
        data['account']['diff'] = diff
        flag = 1
        print(diff)
        if(diff != 0):
          previous[-1][today] = account.followed_by_count
          snap = str(len(previous) - 1)
          print('diff not')
          result = firebse.put(Dataurl+stamp, snap, {today:previous[-1][today]}) 
        break

      if(flag == 0):
        previous.append({ today: account.followed_by_count })
        result = firebse.put(Dataurl, stamp, previous)
        diff = account.followed_by_count - previous[-1][today]
        print('update')
        data['account']['diff'] = diff
        break
  if(newEntry == 0):
    print('new entry')
    Dataurl = 'https://covidai-1dd78.firebaseio.com/covidai-1dd78/followcount/'+username
    firebse.post(Dataurl, [{today: account.followed_by_count}])
      
  return data
  
@app.route('/<username>/coms')
def getcomments(username):
  instagram = Instagram()
  data = {}
  coms = []
  medias = instagram.get_medias(username, 1000)
  for x in medias:
    comments = instagram.get_media_comments_by_id(x.identifier, 10000)
    for comment in comments['comments']:
        coms.append(comment.text)
  data['comments'] = coms
  return data

@app.route('/<username>/likesncoms')
def getlikesncoms(username):
  instagram = Instagram()
  data = {'like_timeline': {},
  'comment_timeline': {}}
  total_likes = 0
  total_comments = 0
  medias = instagram.get_medias(username, 1000)
  flag = 0
  for x in medias:
    timestamp = x.created_time
    dh_object = datetime.fromtimestamp(timestamp).strftime("%H")
    if(flag == 0):
      data['like_timeline'][dh_object] = x.likes_count
      data['comment_timeline'][dh_object] = x.comments_count
    else:
      data['like_timeline'][dh_object] += x.likes_count
      data['comment_timeline'][dh_object] += x.comments_count  
    total_likes += x.likes_count
    total_comments += x.comments_count
  data['total_likes'] = total_likes
  data['total_comments'] = total_comments
  return data

@app.route('/<username>/latest')
def getlatest(username):
  data = {}
  instagram = Instagram()
  medias = instagram.get_medias(username, 1)
  for x in medias:
    data['created_time'] = x.created_time
    data['caption'] = x.caption
    data['likes_count'] = x.likes_count
    data['comments_count'] = x.comments_count
    data['image_high_resolution_url'] = x.image_high_resolution_url
    data['link'] = x.link
  return data

@app.route('/<username>/followtimeline')
def getfollowTimeline(username):
  firebse = firebase.FirebaseApplication('https://covidai-1dd78.firebaseio.com/', None)
  previous = firebse.get('https://covidai-1dd78.firebaseio.com/covidai-1dd78/followcount/'+username, '')
  keys = previous.keys()
  for key in keys:
    timeline = { 'Followtimeline': previous[key] }
  return timeline

@app.route('/trending/<key>')
def getTrending(key):
    text = key
    URL_indian = "http://best-hashtags.com/hashtag/"+text
    r_indian = requests.get(URL_indian) 

    soup_indian = BeautifulSoup(r_indian.content, 'html.parser') 
    hashtag_indian = soup_indian.find('p1').getText().split(" ")[1:11]
    return {"hashtags": hashtag_indian}


if __name__ == '__main__':
  app.run(host='0.0.0.0',port='8001', debug=True)
