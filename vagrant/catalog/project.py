from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants')
def Restaurants():

    output = ""
    output += "<html>"
    output += """
        <head>
        <style>
            a {margin : 10px;}
        </style>
        </head>
        """
    output +="<body>"

    menuItems = session.query(MenuItem).all()
    for mi in menuItems:
        output += "----%s----</br>" % mi.name
        output += "----%s----</br>" % mi.price
        output += "----%s----</br>" % mi.description
                
        output += "<p><a href='menuItems/%s/edit'>Edit</a>" % mi.id
        output += "<a href='restaurants/%s/delete'>Delete</a></p></br>" % mi.id
    output += "</body></html>"

    print("Here here")
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)