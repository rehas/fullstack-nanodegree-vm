from flask import Flask , render_template, url_for, request, redirect, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# List all restaurants
@app.route('/')
@app.route('/restaurants')
def ListRestaurants():
    restaurants = session.query(Restaurant).all()
    output = ""
    for r in restaurants:
        output += r.name
        output += "<hr>"
    return "<p> First Path </p>" + output


# Create a new restaurant
@app.route('/restaurants/new')
def NewRestaurant():
    return "Add New Restaurant"


# Edit given restaurant
@app.route('/restaurants/<int:restaurant_id>/edit')
def EditRestaurant(restaurant_id):
    return "Edit This Restaurant: %s" % restaurant_id


# Delete given restaurant
@app.route('/restaurants/<int:restaurant_id>/delete')
def DeleteRestaurant(restaurant_id):
    return "Delete This Restaurant: %s" % restaurant_id


# List Menu Items of a Restaurant
@app.route('/restaurants/<int:restaurant_id>/menu')
def ListRestaurantMenu(restaurant_id):
    return "Menu for Restaurant: %s is:" % restaurant_id


# Add new menu item to restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/new')
def AddMenuItemToRestaurant(restaurant_id):
    return "This page adds a new menu item to restaurant : %s" %restaurant_id


# Edit menu item of restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/edit')
def EditMenuItem(restaurant_id, menu_item_id):
    return """
        This page edits menu item : %s of the restaurant : %s
    """ % (menu_item_id, restaurant_id)

# Delete menu item of restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/delete')
def DeleteMenuItem(restaurant_id, menu_item_id):
    return """
        This page deletes menu item : %s of the restaurant : %s
    """ % (menu_item_id, restaurant_id)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=4000)