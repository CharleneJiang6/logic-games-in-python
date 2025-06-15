from itertools import combinations


def trois_coloration(sommets: list[str], arcs: list[tuple[str, str]], couleurs: list[str]) -> tuple[str, dict]:
    """genere un texte en format dimacs"""

    # 1/ generer tous les variables à utiliser dans le dimacs
    i = 1
    sommet_couleur: dict[str, int] = {}
    for s in sommets:
        for c in couleurs:
            sommet_couleur[s + c] = i  # eg: S1R : 1, S1V : 2 ...
            i += 1

    # 2/ ecrire la base des clauses
    # indices = [0, 3, 6]  # chaque SiX occupe 3 places. eg: les 3 premiers sont S1X. [S1X, S2X, S3X]
    # variables = list(sommet_couleur.keys())
    # clauses: list[list[str]] = []  # eg: ['S1R', 'S1V', 'S1B'] est une clause
    # for i in indices:
    #     clauses.append([variables[i], variables[i + 1], variables[i + 2]])  # clause "au moins une"
    #
    #     clauses.append(['-' + variables[i], '-' + variables[i + 1]])  # clauses de type : not S1R or not S1V
    #     clauses.append(['-' + variables[i], '-' + variables[i + 2]])
    #     clauses.append(['-' + variables[i + 1], '-' + variables[i + 2]])
    #
    # for i in range(3):  # pour les 3 couleurs : un pas = une couleur differente
    #     clauses.append(['-' + variables[indices[0] + i], '-' + variables[indices[1] + i]])
    #     clauses.append(['-' + variables[indices[0] + i], '-' + variables[indices[2] + i]])
    #     clauses.append(['-' + variables[indices[1] + i], '-' + variables[indices[2] + i]])

    clauses: list[list[str]] = []  # eg: ['S1R', 'S1V', 'S1B'] est une clause

    # CORRECTION:
    for s in sommets:  # au moins 1
        clause = [f"{s}{c}" for c in couleurs]
        clauses.append(clause)

    for s in sommets:  # au plus 1
        for c1, c2 in combinations(couleurs, 2):
            clauses.append([f"-{s}{c1}", f"-{s}{c2}"])

    for s1, s2 in arcs:
        for c in couleurs:
            clauses.append([f"-{s1}{c}", f"-{s2}{c}"])

    prompt = f"c exercice COLORER\np cnf {len(sommet_couleur)} {len(clauses)}\n"
    for clause in clauses:
        for l in clause:
            if l[0] == '-':  # si de la forme -S1R
                prompt += '-' + str((sommet_couleur[l[1:]]))
            else:
                prompt += str(sommet_couleur[l])
            prompt += " "
        prompt += "0\n"

    return prompt, sommet_couleur

    # python tp2.py > tp2.cnf


def solution_lisible(solution: str, correspondances: dict[str, int]) -> str:
    solution = solution.strip().split(" ")
    msg = []
    dico = {v: k for k, v in correspondances.items()}  # inverse le dico
    for i in solution:
        if int(i) > 0:
            msg.append(dico[int(i)])
    return " ".join(msg)


sommets = ["S1", "S2", "S3"]
arcs = [("S1", "S2"), ("S2", "S3"), ("S1", "S3")]
couleurs = ["R", "V", "B"]

if __name__ == "__main__":
    dimacs, som = trois_coloration(sommets, arcs, couleurs)
    # with open("colorer2.cnf", "w") as f:
    #     f.write(dimacs)

    solution = "-1 -2 3 -4 5 -6 7 -8 -9 0"
    print("les couleurs sont : ", solution_lisible(solution, som))

# PS C:\Users\Charlène\IA02\tp2> gophersat colorer.cnf
# c solving colorer.cnf
# s SATISFIABLE
# v -1 -2 3 -4 5 -6 7 -8 -9 0

# Methode de resolution d un pb SAT :
# 1/ definir les variables bool + traduire les contraintes en bases de clauses
# 2/ definir correspondances entre les var bool et 0..n
# 3/ ecrire la liste des clauses, tq une clause est une liste de litteraux : ["S1V", "-S2R"]
# 4/ traduire tout en dimacs
