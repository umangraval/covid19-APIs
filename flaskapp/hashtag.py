import requests

url = "https://api.hashtagify.me/oauth/token"

payload = "grant_type=client_credentials&client_id=CONSUMER_KEY&client_secret=CONSUMER_SECRET"
headers = {
  'cache-control': "no-cache",
  'content-type': "application/x-www-form-urlencoded"
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)

# url1 = "https://api.hashtagify.me/1.0/tag/smm"

# headers = {
#   'authorization': response.text.access_token,
#   'cache-control': "no-cache"
# }

# res = requests.request("GET", url1, headers=headers)

# print(res.text)