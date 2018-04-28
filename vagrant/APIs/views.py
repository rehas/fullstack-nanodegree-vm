from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)




#foursquare_client_id = ''

#foursquare_client_secret = ''

#google_api_key = ''

engine = create_engine('sqlite:///restaruants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
    if request.method == 'GET':
        restaurants = session.query(Restaurant).all()
        return jsonify(restaurants = [r.serialize for r in restaurants])
    if request.method == 'POST':
        location = request.args.get('location')
        mealType = request.args.get('mealType')

        foundRest = findARestaurant(mealType, location)

        newRest = Restaurant( restaurant_name = foundRest['name'])
        newRest.restaurant_address = foundRest['address']
        newRest.restaurant_image = foundRest['image']

        session.add(newRest)
        session.commit()
        #print(foundRest)
        return jsonify(restaurant = newRest.serialize)

  #YOUR CODE HERE
    
@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
    
    return
  #YOUR CODE HERE


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


  