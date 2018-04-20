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
    restaurant = session.query(Restaurant).filter_by(id = id).first()
    return restaurant    


# List all restaurants
@app.route('/')
@app.route('/restaurants')
def ListRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)


# Create a new restaurant
@app.route('/restaurants/new',  methods = ['GET', 'POST'])
def NewRestaurant():
    if request.method == 'GET':
        return render_template('newrestaurant.html')
    else:
        newRestaurant = Restaurant(name = request.form['newRestaurantName'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('ListRestaurants'))


# Edit given restaurant
@app.route('/restaurants/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def EditRestaurant(restaurant_id):
    restaurant = getRestaurant(restaurant_id)
    if request.method == 'GET':
        return render_template('editrestaurant.html', restaurant = restaurant )
    else:
        restaurant.name = request.form['editRestaurantName']
        session.add(restaurant)
        session.commit()
        return redirect(url_for('ListRestaurants'))

# Delete given restaurant
@app.route('/restaurants/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def DeleteRestaurant(restaurant_id):
    restaurant = getRestaurant(restaurant_id)
    if request.method == 'GET':
        return render_template('deleterestaurant.html', restaurant = restaurant)
    else:
        session.delete(restaurant)
        session.commit()
        return redirect(url_for('ListRestaurants'))

# List Menu Items of a Restaurant
@app.route('/restaurants/<int:restaurant_id>/menu')
def ListRestaurantMenu(restaurant_id):
    restaurant = getRestaurant(restaurant_id)
    menu_items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()    
    return render_template('menu.html', restaurant = restaurant, menu_items = menu_items)


# Add new menu item to restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def AddMenuItemToRestaurant(restaurant_id):
    restaurant = getRestaurant(restaurant_id)
    if request.method == 'GET':
        return render_template('newmenuitem.html', restaurant = restaurant)
    else:
        newItem = MenuItem(name = request.form['newMenuItemName'])
        newItem.price = request.form['newMenuItemPrice']
        newItem.description = request.form['newMenuItemDescription']
        newItem.course = request.form['newMenuItemCourse']
        newItem.restaurant_id = restaurant.id
        session.add(newItem)
        session.commit()
        return redirect(url_for('ListRestaurantMenu', restaurant_id = restaurant.id))

# Edit menu item of restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/edit', methods = ['GET', 'POST'])
def EditMenuItem(restaurant_id, menu_item_id):
    restaurant = getRestaurant(restaurant_id)
    menu_item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).filter_by(id = menu_item_id).first()
    if menu_item == None:
        flash("No such Menu Item for That Restaurant Babe!")
        return redirect(url_for('AddMenuItemToRestaurant', restaurant_id = restaurant_id))
        
    if request.method == 'GET':
        return render_template('editmenuitem.html', restaurant = restaurant, menu_item = menu_item)
    else:
        menu_item.name = request.form['editMenuItemName']               or menu_item.name
        menu_item.price = request.form['editMenuItemPrice']             or menu_item.price
        menu_item.description = request.form['editMenuItemDescription'] or menu_item.description
        menu_item.course = request.form['editMenuItemCourse']           or menu_item.course
        session.add(menu_item)
        session.commit()
        return redirect(url_for('ListRestaurantMenu', restaurant_id = restaurant.id))


# Delete menu item of restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/delete', methods = ['GET', 'POST'])
def DeleteMenuItem(restaurant_id, menu_item_id):
    restaurant = getRestaurant(restaurant_id)
    menu_item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).filter_by(id = menu_item_id).first()
    if menu_item == None:
        flash("No such Menu Item for That Restaurant Babe!")
        return redirect(url_for('ListRestaurantMenu', restaurant_id = restaurant_id))
    if request.method == 'GET':
        return render_template('deletemenuitem.html', restaurant = restaurant, menu_item = menu_item)
    else:
        session.delete(menu_item)
        session.commit()
        return redirect(url_for('ListRestaurantMenu', restaurant_id = restaurant.id))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=4000)