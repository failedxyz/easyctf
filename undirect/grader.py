def grade(autogen, key):
    if key.find("1t's_4lw4ys_a_G00d_idea_2_ch3ck_th3_he4d3rs!") != -1:
        return True, "You got it!"
    return False, "Nope. Keep poking around."
