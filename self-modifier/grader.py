def grade(random, key):
    if key.find("Z7a_ok_qfme_xt") != -1:
        return True, "Correct!"
    incorrect_txt = 'Wrong. '
    if key.find("Z7a") == -1:
    	incorrect_txt += "Phase 1 failed. "
    if key.find("_ok_") == -1:
    	incorrect_txt += "Phase 2 failed. "
    if key.find("qfme") == -1:
    	incorrect_txt += "Phase 3 failed. "
    if key.find("_xt") == -1:
    	incorrect_txt += "Phase 4 failed. "
    return False, incorrect_txt
