from flask import render_template, Flask, request, json
from googletrans import Translator
import requests
translator = Translator()

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

if __name__ == '__main__':
  app.run(host='0.0.0.0',port='8001', debug=True)
