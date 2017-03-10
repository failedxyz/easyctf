def grade(autogen, key):
    if key.find("todo") != -1:
        return True, "Awesome job! Get ready for some harder ones :)"
    return False, "Keep trying!"
