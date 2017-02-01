def grade(autogen, answer):
    if answer.find("th3re_R_2_manY_Types_0f_Oboes_4_m3!!!") != -1:
        return True, "Congrats!"
    return False, "Nope, try again."