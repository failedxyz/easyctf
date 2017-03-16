def grade(autogen, key):
    if key.upper().find("CAN_YOU_EVEN_HEAR_ME_YET") != -1:
        return True, "Correct!"
    return False, "Nope!"
