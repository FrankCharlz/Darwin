import os
import urllib

import jinja2
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb


from models.models import Announcement
from models.models import User

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

class RegisterUser(webapp2.RequestHandler):
     def post(self):
         username = self.request.get('username')
         email = self.request.get('email')
         pass1 = self.request.get('pass1')
         pass2 = self.request.get('pass2')

         user = User()
         user.name = username
         user.email = email
         user.password = pass1
         user.id = randint(100000,999999)
         user.group_id = 0

         key = user.put()

         self.redirect('/')








app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/register_user', RegisterUser),
], debug=True)
