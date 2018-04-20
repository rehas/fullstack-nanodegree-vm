from flask import Flask , render_template, url_for, request, redirect, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def getRestaurant(id):
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    return restaurant    


# List all restaurants
@app.route('/')
@app.route('/restaurants')
def ListRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)


# Create a new restaurant
@app.route('/restaurants/new')
def NewRestaurant():
    return render_template('newrestaurant.html')


# Edit given restaurant
@app.route('/restaurants/<int:restaurant_id>/edit')
def EditRestaurant(restaurant_id):
    restaurant = getRestaurant(restaurant_id)
    return render_template('editrestaurant.html', restaurant = restaurant )


# Delete given restaurant
@app.route('/restaurants/<int:restaurant_id>/delete')
def DeleteRestaurant(restaurant_id):
    restaurant = getRestaurant(restaurant_id)
    return render_template('deleterestaurant.html', restaurant = restaurant)


# List Menu Items of a Restaurant
@app.route('/restaurants/<int:restaurant_id>/menu')
def ListRestaurantMenu(restaurant_id):
    restaurant = getRestaurant(restaurant_id)
    menu_items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()    
    return render_template('menu.html', restaurant = restaurant, menu_items = menu_items)


# Add new menu item to restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/new')
def AddMenuItemToRestaurant(restaurant_id):
    restaurant = getRestaurant(restaurant_id)
    return render_template('newmenuitem.html', restaurant = restaurant)


# Edit menu item of restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/edit')
def EditMenuItem(restaurant_id, menu_item_id):
    restaurant = getRestaurant(restaurant_id)
    menu_item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).filter_by(id = menu_item_id).first()
    if menu_item == None:
        flash("No such Menu Item for That Restaurant Babe!")
        return redirect(url_for('AddMenuItemToRestaurant', restaurant_id = restaurant_id))
        
    return render_template('editmenuitem.html', restaurant = restaurant, menu_item = menu_item)

# Delete menu item of restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/delete')
def DeleteMenuItem(restaurant_id, menu_item_id):
    restaurant = getRestaurant(restaurant_id)
    menu_item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).filter_by(id = menu_item_id).first()
    if menu_item == None:
        flash("No such Menu Item for That Restaurant Babe!")
        return redirect(url_for('ListRestaurantMenu', restaurant_id = restaurant_id))
        
    return render_template('deletemenuitem.html', restaurant = restaurant, menu_item = menu_item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=4000)