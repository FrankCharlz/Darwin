
from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    id = ndb.IntegerProperty()
    bio = ndb.StringProperty()
    group_id = ndb.IntegerProperty(default = 0)
    profile_photo_key = ndb.BlobKeyProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class Announcement(ndb.Model):
    user_id =  ndb.IntegerProperty()
    group_id = ndb.IntegerProperty()
    content = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class File(ndb.Model):
    name = ndb.StringProperty()
    user_id =  ndb.IntegerProperty()
    group_id = ndb.IntegerProperty()
    file_key = ndb.BlobKeyProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class Group(ndb.Model):
    id = ndb.IntegerProperty()
    name = ndb.StringProperty()
    description = ndb.TextProperty()
    admin = ndb.StringProperty()
    users = ndb.IntegerProperty(default = 0)
    files = ndb.IntegerProperty(default = 0)
    date = ndb.DateTimeProperty(auto_now_add=True)