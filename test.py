# sample data scrape from wiki
import requests
from bs4 import BeautifulSoup

# website_url = requests.get('https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Spain').text
# soup = BeautifulSoup(website_url,'lxml')
# My_table = soup.find('table',{'class':'wikitable sortable'})
# retJSON = {}
# data = []
# links = My_table.find_all('tr')
# for link in links:
#     dataTag = link.find_all('td')
#     if(len(dataTag) == 9):
#         state = dataTag[0].text.rstrip("\n").replace('(article)','')
#         cases = dataTag[1].text.rstrip("\n")
#         deaths = dataTag[4].text.rstrip("\n")
#         recovered = dataTag[5].text.rstrip("\n")
#         region = {
#             "state": state,
#             "cases": cases,
#             "deaths": deaths,
#             "recovered": recovered
#         }
#         data.append(region)

# website_url = requests.get('https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Italy').text
# soup = BeautifulSoup(website_url,'lxml')
# My_table = soup.find('table',{'class':'wikitable sortable'})
# retJSON = {}
# data = []
# links = My_table.find_all('tr')
# for link in links:
#     dataTag = link.find_all('td')
#     print(len(dataTag))
#     headingTag = link.find_all('th')
#     if(len(headingTag) == 1):
#         state = headingTag[0].text.rstrip("\n")
#         if(state == 'Italy'):
#             state = 'Total'
#         if(len(dataTag) == 10):
#             cases = dataTag[0].text.rstrip("\n")
#             deaths = dataTag[1].text.rstrip("\n")
#             recovered = dataTag[5].text.rstrip("\n")
#             region = {
#                 "state": state,
#                 "cases": cases,
#                 "deaths": deaths,
#                 "recovered": recovered
#             }
#             data.append(region)
# retJSON['data'] = data          

website_url = requests.get('https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Germany').text
soup = BeautifulSoup(website_url,'lxml')
My_table = soup.find('table',{'class':'wikitable mw-collapsible'})
retJSON = {}
data = []
links = My_table.find_all('tr')
for link in links:
    dataTag = link.find_all('td')
    headingTag = link.find_all('th')
    print(headingTag)
    print("\n")
    if(len(headingTag) == 16):
       state = headingTag[0].text.rstrip("\n")
       if(len(dataTag) == 19):
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
print(retJSON)
