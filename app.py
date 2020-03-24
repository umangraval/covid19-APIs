from flask import render_template, Flask, request, json
from googletrans import Translator
translator = Translator()
    
app = Flask(__name__)

@app.route('/translate', methods=['POST', 'GET']) 
def translate():
    if request.method == 'POST':
        text = request.form['text']
        lan = request.form['lan']
        trans = []
        translator.translate(text, dest=lan)
        trans.append(t.text)
        translated = ' '.join(trans)
        # return translated
        return render_template('trans.html', data=translated) 
    else:
        return render_template('trans.html')

@app.route('/')
def home():
  return render_template("home.html")

@app.route('/stats')
def getstats():
  retJSON = requests.get('https://api.rootnet.in/covid19-in/stats/latest')
  data = retJSON.json()
  return data

if __name__ == '__main__':
  app.run(host='0.0.0.0',port='8001')
