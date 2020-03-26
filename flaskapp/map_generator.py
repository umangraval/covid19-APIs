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
    # Load the JSON File and Fetch the Data
    http = urllib3.PoolManager()
    r = http.request('GET', 'https://api.rootnet.in/covid19-in/stats/latest')
    data =  json.loads(r.data.decode('utf-8'))
    new = pd.DataFrame.from_dict(data['data']['regional'])
    print(new.columns)
    # Including the Ladakh UT stats along with Jammu and Kashmir Region Only and other Mofifications
    for x in new.columns[1:]:
        new.loc[new['loc'] == 'Jammu and Kashmir',x] =   int(new.loc[new['loc'] == 'Jammu and Kashmir'][x].values + new.loc[new['loc'] == 'Ladakh'][x].values)
    new.drop(new[new['loc'] == 'Ladakh'].index, inplace = True)
    new.loc[new['loc'] == 'Telengana', 'loc'] = 'Telangana'
    new.loc[new['loc'] == 'Jammu and Kashmir', 'loc'] = 'Jammu & Kashmir'
    new.reset_index(level=0, inplace=True)
    new.drop('index', axis = 1,inplace = True)
    new.columns = ['st_nm', 'confirmedCasesIndian', 'confirmedCasesForeign', 'discharged','deaths']
    states = list(new['st_nm'])


    # ## Initialize the Visualization and Read the Template
    image = cv2.imread('template2.png')
    # image = cv2.resize(image, (1125,1125))
    image[np.where((image==[255,255,255]).all(axis=2))] = [0,0,0];
    sns.set(style = 'whitegrid', palette = 'pastel', color_codes = True)
    figsize = (image.shape[0]/96,image.shape[1]/96)
    sns.set(rc={'figure.figsize':figsize})

    # Read the Shape Files
    shp_path = 'Indian_States.shp'
    sdf = gpd.read_file(shp_path)

    # Considering only the Mainland India and making modifications in dataframe
    sdf.loc[sdf['st_nm'] == 'NCT of Delhi','st_nm'] = 'Delhi'
    sdf = sdf.iloc[1:,:]
    sdf.drop([16], inplace = True)
    sdf.plot(cmap='viridis', scheme='quantiles')

    ssdf = pd.DataFrame(sdf[sdf['st_nm'].isin(states)])
    ssdf.reset_index(level=0, inplace=True)
    ssdf.drop('index', axis = 1, inplace = True)
    print(ssdf)
    st_names = list(ssdf.st_nm)


    # Calculating centroid points
    ssdf['centroid_x'] = 0
    ssdf['centroid_y'] = 0
    ssdf['confirmedCases'] = 0
    print(ssdf.columns)
    print(new.columns)
    for i in ssdf.index:
        st = ssdf.loc[i]['st_nm']
        cc = new.loc[new['st_nm'] == st]['confirmedCasesForeign'].values + new.loc[new['st_nm'] == st]['confirmedCasesIndian'].values
        ssdf.loc[i, 'centroid_x'] = ssdf.loc[i,'geometry'].centroid.x
        ssdf.loc[i, 'centroid_y'] = ssdf.loc[i,'geometry'].centroid.y
        ssdf.loc[i, 'confirmedCases'] = cc

    x_list = list(ssdf['centroid_x'])
    y_list = list(ssdf['centroid_y'])
    confirmedCases = list(ssdf['confirmedCases'])





    plt.axis('off')
    for i,st in enumerate(st_names):
        # print(st)
        if st == 'Punjab':
            plt.text(x_list[i]-2.5,y_list[i]-0.2,st, fontsize=10,fontweight = 'extra bold', color = 'red')
        elif st == "Chandigarh":
            plt.text(x_list[i]+0.5,y_list[i],st, fontsize=10,fontweight = 'extra bold', color = 'red')
        elif st == 'Himachal Pradesh':
            plt.text(x_list[i]+0.3,y_list[i]-0.2,st, fontsize=10,fontweight = 'extra bold', color = 'red')
        elif st == 'Haryana':
            plt.text(x_list[i]-2.75,y_list[i]-0.2,st, fontsize=10,fontweight = 'extra bold', color = 'red')
        elif st == 'Kerala':
            plt.text(x_list[i]-2.25,y_list[i]-0.2,st, fontsize=10,fontweight = 'extra bold', color = 'red')
        else:
            plt.text(x_list[i]+0.5,y_list[i]-0.2,st, fontsize=10,fontweight = 'extra bold', color = 'red')
        plt.scatter(x_list[i],y_list[i],c = 'black', s = 200, marker=r"$ {} $".format(confirmedCases[i]))

    plt.savefig('map.png')
    map = cv2.imread('map.png')
    map = cv2.resize(map, (image.shape[0], image.shape[1]))
    final = image + map
    langs = ['english','telugu','bengali','tamil','malayalam']
    for lan in langs:
        cv2.imwrite('./Posts/Final_'+lan+'.jpg',final)
