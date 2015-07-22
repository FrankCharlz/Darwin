
from code.models import User

def userExists(username):
    q = User.query(User.name == username)
    return q.count()


def emailExists(email):
    q = User.query(User.email == email)
    return q.count()


