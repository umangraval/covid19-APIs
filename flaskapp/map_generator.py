import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pyl
import seaborn as sns
import geopandas as gpd
import io
from PIL import Image
import cv2
import json
import urllib3
# def calc_colour(value):

if __name__ == "__main__":

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
    active = int(total - (recovered + recovered))

    new = pd.DataFrame.from_dict(newdata['data']['regional'])
    print('Data Fetched')

    new.drop(new[new['loc'] == 'Ladakh'].index, inplace = True)
    new.loc[new['loc'] == 'Telengana', 'loc'] = 'Telangana'
    new.loc[new['loc'] == 'Jammu and Kashmir', 'loc'] = 'Jammu & Kashmir'
    new.reset_index(level=0, inplace=True)
    new.drop('index', axis = 1,inplace = True)
    new.columns = ['st_nm', 'confirmedCases', 'discharged','deaths']
    states = list(new['st_nm'])


    ## Initialize the Visualization and Read the Template

    ## English Template
    image_eng = cv2.imread('template2.png')
    image_eng[np.where((image_eng==[255,255,255]).all(axis=2))] = [0,0,0];
    ## Telugu Template
    image_tel = cv2.imread('TELUGU.png')
    image_tel = cv2.resize(image_tel, (image_eng.shape[0], image_eng.shape[1]))
    image_tel[np.where((image_tel==[255,255,255]).all(axis=2))] = [0,0,0];

    sns.set(style = 'whitegrid', palette = 'pastel', color_codes = True)
    figsize = (image_eng.shape[0]/96,image_eng.shape[1]/96)
    sns.set(rc={'figure.figsize':figsize})

    # Read the Shape Files
    shp_path = 'Indian_States.shp'
    sdf = gpd.read_file(shp_path)
    print(sdf)

    # Considering only the Mainland India and making modifications in dataframe
    print('Setting up the Map')
    sdf.loc[sdf['st_nm'] == 'NCT of Delhi','st_nm'] = 'Delhi'
    sdf = sdf.iloc[1:,:]
    sdf.drop([16], inplace = True)
    sdf.boundary.plot(color = 'black')

    ssdf = pd.DataFrame(sdf[sdf['st_nm'].isin(states)])
    ssdf.reset_index(level=0, inplace=True)
    ssdf.drop('index', axis = 1, inplace = True)
    st_names = list(ssdf.st_nm)

    # Calculating centroid points
    ssdf['centroid_x'] = 0
    ssdf['centroid_y'] = 0
    ssdf['confirmedCases'] = 0
    for i in ssdf.index:
        st = ssdf.loc[i]['st_nm']
        cc = new.loc[new['st_nm'] == st]['confirmedCases'].values
        ssdf.loc[i, 'centroid_x'] = ssdf.loc[i,'geometry'].centroid.x
        ssdf.loc[i, 'centroid_y'] = ssdf.loc[i,'geometry'].centroid.y
        ssdf.loc[i, 'confirmedCases'] = cc

    x_list = list(ssdf['centroid_x'])
    y_list = list(ssdf['centroid_y'])
    confirmedCases = list(ssdf['confirmedCases'])

    plt.axis('off')
    for i,st in enumerate(st_names):

        if st == 'Punjab':
            plt.text(x_list[i]-1.5,y_list[i]-0.2,confirmedCases[i], fontsize=15,fontweight = 'extra bold', color = 'red')
        elif st == "Chandigarh":
            plt.text(x_list[i]+0.5,y_list[i],confirmedCases[i], fontsize=15,fontweight = 'extra bold', color = 'red')
        elif st == 'Himachal Pradesh':
            plt.text(x_list[i]+0.3,y_list[i]-0.2,confirmedCases[i], fontsize=15,fontweight = 'extra bold', color = 'red')
        elif st == 'Haryana':
            plt.text(x_list[i]-1.5,y_list[i]-0.2,confirmedCases[i], fontsize=15,fontweight = 'extra bold', color = 'red')
        elif st == 'Kerala':
            plt.text(x_list[i]-2.25,y_list[i]-0.2,confirmedCases[i], fontsize=15,fontweight = 'extra bold', color = 'red')
        elif st == 'West Bengal':

            ## Summary Coordinates
            rx = x_list[i]
            ry = y_list[i]

            plt.text(rx,ry-10,'Total Cases          :',fontsize = 17, fontweight = 'extra bold', color = 'red')
            plt.text(rx,ry-11,'Active Cases        :',fontsize = 17, fontweight = 'extra bold', color = 'red')
            plt.text(rx,ry-12,'Recovered Cases :',fontsize = 17, fontweight = 'extra bold', color = 'red')
            plt.text(rx,ry-13,'Deaths                 :',fontsize = 17, fontweight = 'extra bold', color = 'red')
            plt.text(rx+8.6,ry-10,total,fontsize = 17, fontweight = 'extra bold', color = 'black')
            plt.text(rx+8.6,ry-11,active,fontsize = 17, fontweight = 'extra bold', color = 'black')
            plt.text(rx+8.6,ry-12,recovered,fontsize = 17, fontweight = 'extra bold', color = 'black')
            plt.text(rx+8.6,ry-13,death,fontsize = 17, fontweight = 'extra bold', color = 'black')

            # Mark Number
            plt.text(x_list[i]+0.5,y_list[i]-0.2,confirmedCases[i], fontsize=15,fontweight = 'extra bold', color = 'red')



        else:
            plt.text(x_list[i]+0.5,y_list[i]-0.2,confirmedCases[i], fontsize=15,fontweight = 'extra bold', color = 'red')
        plt.scatter(x_list[i],y_list[i],c = 'black', s = 100, marker='o')


    mine = cv2.imread('map final 2.png')
    plt.savefig('map.png')
    map = cv2.imread('map.png')
    map = cv2.resize(map, (image_eng.shape[0], image_eng.shape[1]))
    map[np.where((image_eng==[255,255,255]).all(axis=2))] = [0,0,0];
    mine = cv2.resize(mine, (image_eng.shape[0], image_eng.shape[1]))
    alpha = 0.4
    added_image = cv2.addWeighted(mine[:,:,:],alpha,map[:,:,:],1-alpha,0)
    final = image_eng + added_image
    final_tel = image_tel + added_image
    langs = ['english','telugu','bengali','tamil','malayalam']
    for lan in langs:
        cv2.imwrite('./Posts/Final_'+lan+'.jpg',final)

