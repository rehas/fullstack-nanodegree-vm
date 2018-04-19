from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>Hello!"
                output += """
                <form method = 'POST' enctype='multipart/form-data' action='/hello'>
                <h2>What would you like me to say?</h2>
                <input name='message' type='text'>
                <input type='submit' value='Submit'>
                </form>
                """
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += """
                <html>
                <body>
                &#161 HOLA !
                <a href = '/hello'> Back to Hello</a>
                """
                output += """
                <form method = 'POST' enctype='multipart/form-data' action='/hello'>
                <h2>What would you like me to say?</h2>
                <input name='message' type='text'>
                <input type='submit' value='Submit'>
                </form>
                """
                output += "</body></html>"

                self.wfile.write(output)
                print(output)
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html>"
                output += """
                <head>
                <style>
                    a {margin : 10px;}
                </style>
                </head>
                """
                output += "<body><h1>Create a New Restaurant</h1>"
                output += """
                    <form method = 'POST' enctype='multipart/form-data' action='/restaurants/new'>
                    <input name='newRestaurantName' type='text'>
                    <input type='submit' value='Create'>
                    </form>
                """
                

                output += "</body></html>"

                self.wfile.write(output)
                print(output)
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

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
                output += "<h2><a href='/restaurants/new'>Create a New Restaurant</a></h2>"

                restaurants = session.query(Restaurant).all()
                for r in restaurants:
                    output += "----%s----" % r.name
                    output += "<p><a href='restaurants/%s/edit'>Edit</a>" % r.id
                    output += "<a href='#'>Delete</a></p></br>"

                output += "</body></html>"

                self.wfile.write(output)
                print(output)
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                rest_id = self.path.split("/")[2]
                rest_edit = session.query(Restaurant).filter_by(id = rest_id).first()
                name = rest_edit.name
                print (rest_id)
                output = ""
                output += "<html>"
                output += """
                <head>
                <style>
                    a {margin : 10px;}
                </style>
                </head>
                """
                output += "<body><h1>Edit Restaurant</h1>"
                output += """
                    <form method = 'POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>
                    <input name='editRestaurantName' type='text' placeholder = '%s'>
                    <input type='submit' value='Edit'>
                    </form>
                """ % (unicode(rest_id), unicode(name))
                

                output += "</body></html>"

                self.wfile.write(output)





        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    newRestaurantName = fields.get('newRestaurantName')

                if(newRestaurantName !=None):
                    print(newRestaurantName[0])
                    newRestaurant = Restaurant(name = newRestaurantName[0] )
                    session.add(newRestaurant)
                    session.commit()
                    output = ""
                    output += "<html><body>"
                    output += "<h2>New Restaurant Added! :</h2>"
                    output += "<h1> %s </h1>" % newRestaurantName[0]
                    output += "<body><h1>Create a New Restaurant</h1>"
                    output += """
                        <form method = 'POST' enctype='multipart/form-data' action='/restaurants'>
                        <input name='newRestaurantName' type='text'>
                        <input type='submit' value='Create'>
                        </form>
                    """
                    output += "</body></html>"
                    self.send_response(301)
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    self.wfile.write(output)
                    print output

            if self.path.endswith("/hello"):
                self.send_response(301)
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')

                if (messagecontent != None):
                    print(messagecontent[0])
                    output = ""
                    output += "<html><body>"
                    output += "<h2>Okay how 'bout this! :</h2>"
                    output += "<h1> %s </h1>" % messagecontent[0]

                    output += """
                        <form method = 'POST' enctype='multipart/form-data' action='/hello'>
                        <h2>What would you like me to say?</h2>
                        <input name='message' type='text'>
                        <input type='submit' value='Submit'>
                        </form>
                    """

                    output += "</body></html>"
                    self.wfile.write(output)
                    print output

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    editRestaurantName = fields.get('editRestaurantName')
                rest_id = self.path.split("/")[2]

                print(editRestaurantName[0])
                editRestaurant = session.query(Restaurant).filter_by(id = rest_id).first()
                editRestaurant.name = editRestaurantName[0]
                session.add(editRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Location', '/restaurants')
                self.end_headers()
            
        except IOError:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print ("Webservice is running through port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print ("^C pressed, stopping we server...")
        server.socket.close()

if __name__ == '__main__':
    main()
