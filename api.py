import requests
from bs4 import BeautifulSoup

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
print(data)
