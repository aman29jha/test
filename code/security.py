from werkzeug.security import safe_str_cmp
from user import User

def authenticate(username, password):
    user = User.findbyusername(username)
    if user and safe_str_cmp(user.password, password) :
        return user

def identity(payload) :
    user_id = payload['identity']
    return User.findbyuserid(user_id)



