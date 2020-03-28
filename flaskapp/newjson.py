import requests, json
import urllib3

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
print(newdata)