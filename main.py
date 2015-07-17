import os
import urllib

import jinja2
import webapp2

from google.appengine.ext import ndb
from google.appengine.ext import blobstore


from models.models import Announcement
from models.models import User
from models.models import File

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
    if q>0:
        return True
    return False


def emailExists(email):
    q = User.query(User.name == email)
    if q>0:
        return True
    return False


class RegisterUser(webapp2.RequestHandler):
    def post(self):
        username = self.request.get('username')
        email = self.request.get('email')
        password = self.request.get('pass')

        a = userExists(username)
        b = emailExists(email)

        if userExists(username) or emailExists(email):
            #username or email already in use
            self.redirect('/register_failed')
        else:
            user = User()
            user.name = username
            user.email = email
            user.password = password
            user.id = randint(100000,999999)
            user.group_id = 0
            key = user.put()
            self.response.write(a,b)
            self.redirect('/new_user_home')








app = webapp2.WSGIApplication([
                                  ('/', MainPage),
                                  ('/register_user', RegisterUser),
                                  ], debug=True)
