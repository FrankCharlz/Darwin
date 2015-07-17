
from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    id = ndb.IntegerProperty()
    group_id = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class Announcement(ndb.Model):
    user_id =  ndb.IntegerProperty()
    group_id = ndb.IntegerProperty()
    content = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class File(ndb.Model):
    user_id =  ndb.IntegerProperty()
    group_id = ndb.IntegerProperty()
    size = ndb.IntegerProperty()
    file_key = ndb.BlobKeyProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)