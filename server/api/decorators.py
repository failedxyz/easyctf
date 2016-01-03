import json
import traceback

from functools import wraps
from flask import session

class WebException(Exception): pass

def api_wrapper(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        web_result = {}
        response = 200
        try:
            web_result = f(*args, **kwds)
        except WebException as error:
            response = 200
            web_result = { "success": 0, "message": str(error) }
        except Exception as error:
            response = 200
            traceback.print_exc()
            web_result = { "success": 0, "message": "Something went wrong! Please notify us about this immediately. %s: %s" % (error, traceback.format_exc()) }
        return json.dumps(web_result), response, { "Content-Type": "application/json; charset=utf-8" }
    return wrapper

import user # Must go below api_wrapper to prevent import loops

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not user.is_logged_in():
            return { "success": 0, "message": "Not logged in." }
        return f(*args, **kwargs)
    return decorated_function

def admins_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not user.is_admin():
            return { "success": 0, "message": "Not authorized." }
        return f(*args, **kwargs)
    return decorated_function
