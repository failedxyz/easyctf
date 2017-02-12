def grade(autogen, key):
    if key.find("Paris,Blair") != -1:
        return True, "Correct!"
    return False, "Nope!"
