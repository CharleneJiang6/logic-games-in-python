from itertools import combinations


def trois_coloration(sommets: list[str],
                     arcs: list[tuple[str, str]], couleurs: list[str]) -> tuple[str, dict]:
    """Génère un texte en format DIMACS"""

    i = 1
    sommet_couleur: dict[str, int] = {}
    for s in sommets:
        for c in couleurs:
            sommet_couleur[s + c] = i  # eg: S1R : 1, S1V : 2 ...
            i += 1

    clauses: list[list[str]] = []  # eg: ['S1R', 'S1V', 'S1B'] est une clause

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


def solution_lisible(sol: str, correspondances: dict[str, int]) -> str:
    solution = sol.strip().split(" ")
    msg = []
    dico = {v: k for k, v in correspondances.items()}  # inverse le dico
    for i in solution:
        if int(i) > 0:
            msg.append(dico[int(i)])
    return " ".join(msg)


def main():
    sommets = ["S1", "S2", "S3"]
    arcs = [("S1", "S2"), ("S2", "S3"), ("S1", "S3")]
    couleurs = ["R", "V", "B"]

    # Ecrire le fichier DIMACS correspondant
    dimacs, som = trois_coloration(sommets, arcs, couleurs)
    with open("colorer.cnf", "w", encoding="utf-8") as f:
        f.write(dimacs)

    # Copier la solution
    solution = "-1 -2 3 -4 5 -6 7 -8 -9 0"
    print("les couleurs sont : ", solution_lisible(solution, som))


if __name__ == "__main__":
    main()

# Execution :
# gophersat colorer.cnf
# c solving colorer.cnf
# s SATISFIABLE
# v -1 -2 3 -4 5 -6 7 -8 -9 0
