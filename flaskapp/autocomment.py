from igramscraper.instagram import Instagram
from firebase import firebase 
from pprint import pprint
instagram = Instagram()
firebase = firebase.FirebaseApplication('https://covidai-1dd78.firebaseio.com/', None)
data = firebase.get('/covidai-1dd78/latest_media/-M3f_ZqzLKNGLoqFP5Mr', '')
print(data)
# authentication supported
instagram.with_credentials('covid.ai', 'CoronaCann09')
instagram.login()

media = instagram.get_medias_from_feed('carona_stats', 1)
print("\n")
for m in media:
    if m.identifier != data['medias']:
        result = firebase.put('/covidai-1dd78/latest_media/-M3f_ZqzLKNGLoqFP5Mr', 'medias', m.identifier)
        comment = instagram.add_comment(m.identifier, 'follow @covid.ai')
