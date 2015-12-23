from functools import wraps
from flask import session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

def admins_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
	return f(*args, **kwargs)
    return decorated_function

def check_csrf(f):
    @wraps(f)
    @login_required
    def wrapper(*args, **kwds):
	return f(*args, **kwds)
    return wrapper
