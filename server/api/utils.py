import datetime
import MySQLdb
import random
import string

from werkzeug.security import generate_password_hash, check_password_hash

host = "localhost"
user = "root"

conn = MySQLdb.connect()

def get_connection():
    global conn
    if not conn:
        conn = MySQLdb.connect(host=host, user=user)
    return conn

def hash_password(s):
    return generate_password_hash(s)

def check_password(hashed_password, try_password):
    return check_password_hash(hashed_password, try_password)

def generate_string(length):
    return "".join([random.choice(string.letters + string.digits) for x in range(length)])

def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0

def get_time_since_epoch():
    return unix_time_millis(datetime.datetime.now())
