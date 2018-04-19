from flask import Flask , render_template, url_for, request, redirect, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    #editUrl = 
    #deleteUrl = url_for('deleteMenuItem')
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
        
    return render_template('menu.html', restaurant = restaurant, items= items)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['newMenuItemName'])
        newItem.price = request.form['newMenuItemPrice']
        newItem.description = request.form['newMenuItemDescription']
        newItem.restaurant_id = restaurant_id

        session.add(newItem)
        session.commit()
        flash("New menu Item Created Bon Appetit!")

        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else :
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        # output = ''
        # output += '<html><body>'
        # output += '<h2>Create New Menu Item For Restaurant: %s</h2>' % restaurant.name
        # output += """ 
        #     <form method = 'POST' enctype='multipart/form-data' action='/restaurants/%s/new'>
        #     <input name='newMenuItemName' type='text' placeholder = "Menu Item Name"></br>
        #     <input name='newMenuItemPrice' type='text' placeholder = "Menu Item Price"></br>
        #     <input name='newMenuItemDescription' type='text' placeholder = "Menu Item Description"></br>
        #     <input type='submit' value='Create'>
        #     </form>
        # """ % restaurant.id   
        # output += '</body></html>'
        return render_template('newMenuItem.html', restaurant = restaurant)


# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    
    if request.method == 'POST':
        menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
        menuItem.name = request.form['editMenuItemName']
        menuItem.price = request.form['editMenuItemPrice']
        menuItem.description = request.form['editMenuItemDescription']
        print(menuItem)
        session.add(menuItem)
        session.commit()
        flash("Menu Item Edited Bon Appetit!")
        
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant = restaurant, item = item)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete' , methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    del_menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(del_menuItem)
        session.commit()
        flash("Menu Item Deleted :( Bon Appetit!")
        
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', item = del_menuItem )

@app.route('/restaurants/<int:restaurant_id>/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/JSON')
def menuItemJson(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem = item.serialize)
    

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)