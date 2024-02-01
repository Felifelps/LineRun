import os
base = os.getcwd() 
class Score:
    global score_path
    score_path = base + ("" if "Source" in base else "\\Source") + "\\GameBase\\score"
    
    def calculate_score(level, time):
        return (level*20) - (time*2)

    def get_best_score():
        r = ""
        for file in os.walk(os.getcwd()):
            if "score" in file[2]: #0-> dir path; 1-> subdirs; 2-> files 
                with open(os.path.join(score_path), "r") as arq:
                    r = arq.read()
                    if r.isdigit():
                        return int(r)
                break
        if r == "":
            with open(os.path.join(score_path), "w") as arq:
                arq.write("0")


    def save_score(score):
        with open(os.path.join(score_path), "w") as arq:
            arq.write(str(score))

