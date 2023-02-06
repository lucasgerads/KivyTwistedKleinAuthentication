from klein import Klein
from twisted.web.static import File
from twisted.web.util import redirectTo
from twisted.internet.defer import succeed
import random
import json
from hashlib import pbkdf2_hmac

webapp = Klein()

requestCounter = 0

from kivy.app import App

@webapp.route('/')
def root(request):
    return redirectTo(b"index", request)

@webapp.route('/index')
def index(request):
    global requestCounter 
    requestCounter += 1
    app = App.get_running_app()
    app.handle_message(requestCounter)
    return File("index.html")

@webapp.route('/assets/<filename>')
def assets(request, filename):
    path = "assets/" + filename
    return File(path) 

@webapp.route('/login')
def login(request):
    return File("login.html")

@webapp.route('/success')
def success(request):
    return File("success.html")

@webapp.route('/fail')
def fail(request):
    return File("fail.html")

@webapp.route('/submit', methods=['POST'])
def submit(request):
    requestResponse = request.content.read()
    password = requestResponse.decode("utf-8").split('=')
    userPassword = pbkdf2_hmac('sha256', password[1].encode('utf-8'), b'some salt'*2, 1000)
    storedPassword =  pbkdf2_hmac('sha256', b'1234', b'some salt'*2, 1000)
    if (userPassword == storedPassword ):
        request.redirect('/success')
        return succeed(None)
    else:
        request.redirect('/fail')
        return succeed(None)

@webapp.route('/protected')
def protected(request):
    return File("protected.html")

@webapp.route('/api/random')
def randomData(request):
    # how do i make this a protected route
    data = {}
    someData = []
    for i in range(10):
        someData.append(random.randrange(start = 0, stop = 100, step=1))
    data['apidata'] = someData
    json_data = json.dumps(data)
    print(json_data)
    return json_data 
