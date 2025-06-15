import itertools

def generate_cnf(sommets, couleurs, liste_arc):
    voc = {}
    clauses = []
    n = 1

    # Création du vocabulaire
    for sommet in sommets:
        for couleur in couleurs:
            voc[sommet + couleur] = n
            n += 1

    # Au moins une couleur par sommet
    for s in sommets:
        clause = [f"{s}{c}" for c in couleurs]
        clauses.append(clause)

    # Au plus une couleur par sommet
    for s in sommets:
        for c1, c2 in itertools.combinations(couleurs, 2):
            clauses.append([f"-{s}{c1}", f"-{s}{c2}"])

    # Contraintes pour les arêtes
    for (u, v) in liste_arc:
        for c in couleurs:
            clauses.append([f"-{u}{c}", f"-{v}{c}"])

    # Affichage en CNF
    dimacs = f"p cnf {len(voc)} {len(clauses)}\n"
    for clause in clauses:
        dimacs += " ".join(str(voc[l]) if l[0] != '-' else str(-voc[l[1:]]) for l in clause) + " 0\n"

    return dimacs, voc

# Conversion de la solution en un format lisible
def convert_solution(solution, voc):
    couleurs_assignées = {}
    for val in solution:
        if val > 0:
            for key, num in voc.items():
                if num == val:
                    sommet = key[:-1]  # Enlever la couleur
                    couleur = key[-1]  # Récupérer la couleur
                    couleurs_assignées[sommet] = couleur
    return couleurs_assignées


sommets = ["S1", "S2", "S3"]
couleurs = ["R", "V", "B"]
liste_arc = [("S1", "S2"), ("S2", "S3"), ("S1", "S3")]
cnf_output, vocabulaire = generate_cnf(sommets, couleurs, liste_arc)

# Écriture dans un fichier
with open("coloration.cnf", "w") as f:
    f.write(cnf_output)

# Résultat de gophersat
solution = [-1, -2, 3, -4, 5, -6, 7, -8, -9]

# Convertir la solution en format lisible
resultat = convert_solution(solution, vocabulaire)

# Affichage des résultats
for sommet, couleur in resultat.items():
    print(f"{sommet} : {couleur}")

"""
Execution + Conclusion : 
gophersat.exe C:/Users/nickp/Desktop/IA02/TP2/coloration.cnf
c solving C:/Users/nickp/Desktop/IA02/TP2/coloration.cnf
s SATISFIABLE
v -1 -2 3 -4 5 -6 7 -8 -9 0
==> 
S1 : bleu
S2 : vert
S3 : rouge
"""