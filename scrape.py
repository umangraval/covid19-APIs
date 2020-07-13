from igramscraper.instagram import Instagram

instagram = Instagram()
data = { 'account': {}}
# authentication supported
# instagram.with_credentials('covid.ai', 'CoronaCann09')
# instagram.login()

# #Getting an account by id
account = instagram.get_account('covid.ai')
data['account']['id'] = account.identifier
data['account']['username'] = account.username
data['account']['Full name'] = account.full_name
data['account']['Biography'] = account.biography
data['account']['Profile pic url'] = account.get_profile_picture_url()
data['account']['Number of published posts'] = account.media_count
data['account']['Number of followers'] = account.followed_by_count
data['account']['Number of follows'] = account.follows_count

total_likes = 0
total_comments = 0
coms = []
medias = instagram.get_medias("covid.ai", 1000)
for x in medias:
    total_likes += x.likes_count
    total_comments += x.comments_count
    comments = instagram.get_media_comments_by_id(x.identifier, 10000)
    for comment in comments['comments']:
        coms.append(comment.text)
data['comments'] = coms
data['total_likes'] = total_likes
data['total_comments'] = total_comments
print(data)
# likes = instagram.get_media_likes_by_code('B-1X4J1psWX', 100)
# # or simply for printing use 
# print(account)
# for like in likes['accounts']:
# print(likes)

# comments = instagram.get_media_comments_by_id('2284384429665556331', 10000)

# for comment in comments['comments']:
#     print(comment.text)

