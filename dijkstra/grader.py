def grade(tid, answer):
    if answer.find("edsger_wybe_dijkstra_was_a_happy_accident") != -1:
        return { "correct": True, "message": "Great Job! That's a tough one." }
    return { "correct": False, "message": "Nope, try again." }