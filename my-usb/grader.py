def grade(autogen, answer):
    if answer.find("d3let3d_f1l3z_r_k00l") != -1:
        return { "correct": True, "message": "Correct!" }
    return { "correct": False, "message": "Nope, try again." }