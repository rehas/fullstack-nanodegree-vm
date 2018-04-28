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

        if foundRest == "FourSquare can't find any results" or foundRest == "FourSquare is not responding":
            return jsonify({"Error": "No restaurants found for %s in %s" % (mealType, location)})

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
    if request.method == 'GET':
        restaurant = session.query(Restaurant).filter_by(id = id).first()
        return jsonify(restaurant = restaurant.serialize)

    if request.method == 'PUT':
        restaurant = session.query(Restaurant).filter_by(id = id).first()
        restaurant.restaurant_name = request.args.get('name') or restaurant.restaurant_name        
        restaurant.restaurant_address = request.args.get('location') or restaurant.restaurant_address        
        restaurant.restaurant_image = request.args.get('image') or restaurant.restaurant_image
        session.add(restaurant)
        session.commit()
        return jsonify(restaurant = restaurant.serialize)
        
    if request.method == 'DELETE':
        restaurant = session.query(Restaurant).filter_by(id = id).first()
        session.delete(restaurant)
        session.commit()        
        return jsonify(restaurant = restaurant.serialize)
        

  #YOUR CODE HERE


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


  