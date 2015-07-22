import os
import urllib

import jinja2
import webapp2
import json

from google.appengine.ext import ndb
from google.appengine.ext import blobstore


from code.models import Announcement
from code.models import User
from code.models import File

from random import randint

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    return ndb.Key('Guestbook', guestbook_name)



class MainPage(webapp2.RequestHandler):

    def get(self):

        users = User.query()
        template_values = {
            'number': randint(10,99),
            'users' : users
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


def userExists(username):
    q = User.query(User.name == username)
    return q.count()


def emailExists(email):
    q = User.query(User.email == email)
    return q.count()


class RegisterUser(webapp2.RequestHandler):
    def post(self):
        username = self.request.get('username')
        email = self.request.get('email')
        password = self.request.get('pass')

        self.response.headers['Content-Type'] = 'application/json'
        response = {}

        if (not username) or (not email) or (not password):
            response['success'] = 0
            response['message'] = 'Field(s) empty'

        elif emailExists(email):
            response['success'] = 0
            response['message'] = 'Email already used'

        elif userExists(username):
            response['success'] = 0
            response['message'] = 'Username already in use'

        else:
            user = User()
            user.name = username
            user.email = email
            user.password = password
            user.id = randint(100000,999999)
            user.group_id = 0
            key = user.put()

            response['success'] = 1
            response['message'] = 'id:'+str(user.id)+',key:'+str(key)

        self.response.write(json.dumps(response))


class Login(webapp2.RequestHandler):
    def post(self):
        username_or_email = self.request.get('username_or_email')
        password = self.request.get('pass')

        self.response.headers['Content-Type'] = 'application/json'
        response = {}

        username = ''
        email = ''

        if (not username_or_email) or (not password):
            response['success'] = 0
            response['message'] = 'Field(s) empty'

        elif '@' in username_or_email:
            #it is an email...
            email = username_or_email
            response['email'] = email
            query = User.query(ndb.AND(User.email == email, User.password == password))
            response['success'] = query.count()
        else:
            #it is a user name
            username = username_or_email
            response['username'] = username
            query = User.query(ndb.AND(User.name == username, User.password == password))
            response['success'] = query.count()

        self.response.write(json.dumps(response))





app = webapp2.WSGIApplication([
                                  ('/', MainPage),
                                  ('/register_user', RegisterUser),
                                  ('/login', Login),
                                  ], debug=True)























