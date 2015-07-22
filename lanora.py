import urllib

import jinja2
import webapp2
import json
from random import randint

from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from utils import *


from code.models import Announcement
from code.models import Group
from code.models import File


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


class CreateGroup(webapp2.RequestHandler):
    def post(self):
        group_name = self.request.get('group_name')
        description  = self.request.get('description')

        self.response.headers['Content-Type'] = 'application/json'
        response = {}

        if (not group_name):
            response['success'] = 0
            response['message'] = 'Field(s) empty'

        else:
            group = Group()
            group.name = group_name
            group.id = randint(100000,999999)
            group.description  = description
            group.users = 1;
            key = group.put()

            response['success'] = 1
            response['message'] = 'id:'+str(group.id)+',key:'+str(key)

        self.response.write(json.dumps(response))

class UploadFile(webapp2.RequestHandler):
    def post(self):
        file_name = self.request.get('file_name')
        file  = self.request.get('file')

        self.response.headers['Content-Type'] = 'application/json'
        response = {}

        if (not file_name):
            response['success'] = 0
            response['message'] = 'Field(s) empty'

        else:
           f = File()
           f.name = file_name
           f.user_id = 0
           f.group_id = 0
           f.put()


        self.response.write(json.dumps(response))


