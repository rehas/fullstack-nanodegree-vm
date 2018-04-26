from geo_code import getGCL
import httplib2
import json
import datetime

import sys
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

fsqr_client_id  = "S5BDBPDBZ3ZAONNKA32SPLD14DK3L2QLT14T144RYDJJZ04E"  
fsqr_client_scr = "TVUBMJXG53P0OYKABVPVYT2PCOQZXUA2BLEWOAM1EJZWPXR5"

defImageUrl = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/\
cheeseburger-34314_1280.png?direct"

def findARestaurant(meal, location):
    latitude, longitude = getGCL(location)

    # print("Latitude => %s ") % latitude 
    # print("Longitude => %s ") % longitude

    url = "https://api.foursquare.com/v2/venues/explore?"
    url += "client_id=S5BDBPDBZ3ZAONNKA32SPLD14DK3L2QLT14T144RYDJJZ04E"
    url += "&client_secret=TVUBMJXG53P0OYKABVPVYT2PCOQZXUA2BLEWOAM1EJZWPXR5"
    url += "&ll=%s,%s" % (latitude, longitude)
    dateList = datetime.date.today().isoformat().split("-")
    date = "".join(dateList)
    url += "&query=%s&limit=1" % meal
    url += "&v=%s" % date

    # print(url)

    h = httplib2.Http()
    response, content = h.request(url, 'GET')

    result = json.loads(content)

    # print(response)
    # print("\n\n\n\n\n\n")
    # print(response['status'])
    # print("\n\n\n\n\n\n below is response meta code:")
    # print(result['meta']['code'])

    if response['status'] != '200':
        return "FourSquare is not responding"
    if result['meta']['code'] != 200:
        return "FourSquare can't find any results"
    
    # print("\n\n\n\n\n\n below is response data")
    # print(result['response']['groups'][0]['items'][0]['venue'])
    # print("\n\n\n\n\n\n")
    # print("\n\n\n\n\n\n")
    #print (result)

    # Restaurant data, id address and name retrieved
    rest_data = result['response']['groups'][0]['items'][0]['venue']
    rest_name = rest_data['name']
    # print("Restaurant Name is : %s") % rest_name
    
    rest_Add_Arr = rest_data['location']['formattedAddress']
    rest_Address = ", ".join(rest_Add_Arr)
    # print("Restaurant Address is : %s") % rest_Address

    rest_id = rest_data['id']
    # Restaurant Image retrieved
    img_url = "https://api.foursquare.com/v2/venues/%s/photos?" % rest_id
    img_url += "client_id=S5BDBPDBZ3ZAONNKA32SPLD14DK3L2QLT14T144RYDJJZ04E"
    img_url += "&client_secret=TVUBMJXG53P0OYKABVPVYT2PCOQZXUA2BLEWOAM1EJZWPXR5"
    img_url += "&v=%s" % date
        
    h = httplib2.Http()
    img_res, img_cont = h.request(img_url, 'GET')

    img_data = json.loads(img_cont)

    if  (img_data['response']['photos']['count'] < 1):
        rest_image = defImageUrl
    else:
        img_link =  img_data['response']['photos']['items'][0]['prefix']
        img_link += str(img_data['response']['photos']['items'][0]['width'])
        img_link += 'x'
        img_link += str(img_data['response']['photos']['items'][0]['height'])
        img_link += img_data['response']['photos']['items'][0]['suffix']
        rest_image = img_link
    
    # print("IMAGE LINK IS => \n")
    # print(rest_image)
    
    print("--------------------RESULT---------------\n")
    print("Restaurant Name => \n %s") % rest_name
    print("Restaurant Address => \n %s ") % rest_Address
    print("Restaurant image url => \n %s") % rest_image

    restaurant = {}

    restaurant["name"] = rest_name
    restaurant["address"] = rest_Address
    restaurant["image"] = rest_image

    return restaurant


if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney Australia")