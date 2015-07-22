import os
import urllib

import jinja2
import webapp2
import json

from google.appengine.ext import ndb
from google.appengine.ext import blobstore

from lanora import *


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


app = webapp2.WSGIApplication([
                                  ('/', MainPage),
                                  ('/register_user', RegisterUser),
                                  ('/login', Login),
                                  ('/create_group', CreateGroup),
                                  ('/upload_file', UploadFile),
                                  ], debug=True)























