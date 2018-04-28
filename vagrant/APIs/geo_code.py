import httplib2
import json
import random

google_api_key = ""

keys = ["AIzaSyC2ewp8AQT1KqI7h3OMdpbx4WoAiJtLRKw",\
            "AIzaSyCzOTa2TsozM93OKpW8G8KPvox6L0etIgE",\
            "AIzaSyDAvjs2oEJ8jIG4OV_dORjZgfi1t1Ox9uE",\
            "AIzaSyBzh7UpaEvqRm2zx0iX2szI9mYNPaPuGDc",\
            "AIzaSyCd2ImsnE1V0-cxRoG84vnU6Zq0TVSJEpA",\
            "AIzaSyBqcXLTDW0EPn_WkZ64D_9FujvkAj4emB4",\
            "AIzaSyCZReoh84TsK-SAaAtN_XqFX7TI7aQNhew",\
            "AIzaSyAJhKNYzDWNTx-BsDCCLyArfOdQff2M3QQ"]

def getGCL(inputString):

    # google_api_key = random.choice(keys)

    # print(google_api_key)
    # print("\n")
    locationString = inputString.replace(" ", "+")
    #url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' %(locationString, google_api_key))
    #h = httplib2.Http()
    
    result = getResponse(locationString)
    # print("Result First Time")
    # print(result)
    
    while result['status'] == 'REQUEST_DENIED':
        i =1
        result = getResponse(locationString)
        # print("Result %s Time") % i
        # print(result)
        i += 1

    if result['status'] == 'ZERO_RESULTS':
        return "ZERO_RESULTS","ZERO_RESULTS"
    #print(url)
    #response, content = h.request(url, 'GET')
    #result = json.loads(content)
    print (result)
    # print("\n\n STATUS => %s") %result['status']
    # print("\n")
    #print (result)

    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']

    # print ("LATITUDE = %s") % latitude
    # print ("LONGITUDE = %s") % longitude
    
    return latitude, longitude

def getResponse(qry):
    google_api_key = random.choice(keys) 
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (qry, google_api_key))
    # print(url)
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content)
    google_api_key = ""
    return result
#getGeoCodeLocation("Ankara Turkey")