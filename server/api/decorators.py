import json
import traceback

from functools import wraps
from flask import session

class WebException(Exception): pass

def admins_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session and not session["admin"]:
            return { "success": 0, "message": "Not authorized." }
        return f(*args, **kwargs)
    return decorated_function

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
            web_result = { "success": 0, "message": "Something went wrong! Please notify us about this immediately.", str(error): traceback.format_exc() }
        return json.dumps(web_result), response, { "Content-Type": "application/json; charset=utf-8" }
    return wrapper
