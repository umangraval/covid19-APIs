import requests, json

url = "https://api.ritekit.com/v1/search/trending?green=1&corona=1"
hashtags = []
response = requests.request("GET", url)
data = json.loads(response.text)
for hashtag in data['tags']:
  hashtags.append("#"+hashtag['tag'])
hashtags = " ".join(hashtags)
print(hashtags)