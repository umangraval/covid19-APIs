import pandas as pd
import io
from PIL import Image, ImageDraw, ImageFont
import json
import urllib3
import os


if __name__ == "__main__":

    print('Fetching Data...')

    http = urllib3.PoolManager()
    r = http.request('GET', 'https://api.covid19india.org/data.json')
    data =  json.loads(r.data.decode('utf-8'))
    newdata = {
        "success": "true",
        "data":{
            "summary":{},
            "regional":[]
        }
    }
    states = data["statewise"]
    for state in states:
        if(state["state"] == "Total"):
            tt = {}
            tt["total"] = state["confirmed"]
            tt["discharged"] = state["recovered"]
            tt["deaths"] = state["deaths"]
            newdata["data"]["summary"] = tt
        else:
            st = {}
            st["loc"] = state["state"]
            st["confirmedCases"] = state["confirmed"]
            st["discharged"] = state["recovered"]
            st["deaths"] = state["deaths"]
            newdata["data"]["regional"].append(st)

    # Getting the Summary Stats
    total = int(newdata['data']['summary']['total'])
    recovered = int(newdata['data']['summary']['discharged'])
    death = int(newdata['data']['summary']['deaths'])
    active = int(total - (recovered + death))

    summ = [total, active, recovered, death]



    new = pd.DataFrame.from_dict(newdata['data']['regional'])
    print('Data Fetched')


    print('Reading Points File....')
    points_file = pd.read_csv('via_export_csv.csv')
    states = list(points_file.region_id)


    cx = []
    cy = []
    print('Generating the Image....')
    for i in range(len(states)):
        cx.append(json.loads(points_file.region_shape_attributes[i])['cx'])
        cy.append(json.loads(points_file.region_shape_attributes[i])['cy'])

    os.replace("./NEW.png", "./Posts/NEW.png")
    back = Image.open('./Posts/NEW.png')
    draw = ImageDraw.Draw(back)
    font = ImageFont.truetype("Fonts/Rajdhani-Bold.ttf", 20)
    for i,st in enumerate(states[:-4]):
        count = new.loc[new['loc'] == st]['confirmedCases'].values
        count = int(count[0])
        if count !=0:
            draw.text((cx[i], cy[i]), str(count), font=font, fill = 'red')

    j = 0
    for i in range(37,41):
        draw.text((cx[i], cy[i]-4), str(summ[j]), font=font, fill = 'red')
        j+=1

    lang = ['english', 'tamil', 'telugu', 'bangali', 'malayalam']
    for lan in lang:
        back = back.convert("RGB")
        back.save('./Posts/'+lan+'.jpg')
    os.replace("./Posts/NEW.png", "./NEW.png")
    print('Images Generated')
