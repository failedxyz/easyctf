def grade(autogen, answer):
    if answer.find("edsger_wybe_dijkstra_was_a_happy_accident") != -1:
        return True, "Great Job! That's a tough one."
    return False, "Nope, try again."