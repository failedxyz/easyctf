import os

with open(".secret_key", "a+") as secret:
    if not secret.read():
        secret.seek(0)
        key = os.urandom(128)
        secret.write(key)
        secret.flush()
    else:
        key = secret.read()

SECRET = key
CTF_BEGIN = 0 # To be used later
CTF_END = 0 # To be used later
