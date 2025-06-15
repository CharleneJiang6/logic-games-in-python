#ds itertools : combination(couleurs,2), avec des for
from itertools import combinations

def trois_coloration(alpha, beta):
    pass

sommets = ["S1", "S2", "S3"]
arcs = [("S1, S2"), ("S2", "S3"), ("S1","S3")]
couleurs = ["R", "V","B"]

i=0
somColor = {}
for s in sommets:
    for c in couleurs:
        somColor[s+c]=i
        i+=1

for i in somColor.items():
    print(i)

# print(list(somColor.keys())[0])

clauses = [] #list of list of clauses
for i in (0,3,6):
    som = list(somColor.keys())
    # print(som)
    clauses.append([som[i], som[i+1],som[i+2]])
    clauses.append(['-'+som[i], '-'+som[i+1]])
    clauses.append(['-'+som[i], '-'+som[i+2]])
    clauses.append(['-'+som[i+1], '-'+som[i+2]])

indices = [0,3,6]
for i in range(3):
    som = list(somColor.keys())
    # print(som)
    clauses.append(['-'+som[indices[0]+i], '-'+som[indices[1]+i]])
    clauses.append(['-'+som[indices[0]+i], '-'+som[indices[2]+i]])
    clauses.append(['-'+som[indices[1]+i], '-'+som[indices[2]+i]])


#CORRECTION: r2: a plus une couleur par sommet
# for s in sommets:
#     for c1,c2 in combinations(couleurs,2):
#         clauses.append(f"-{s}{c1}",f"-{s}{c2}")

# for s1,s2 in arcs:
#     for c in couleurs:
#         clauses.append(f"-{s1}{c}",f"-{s2}{c}")

# dimacs = f"""c
# c
# c
# p cnf {len(somColor)} {len(clauses)}
# """

# for l in clauses:
#     if l[0]=="-":
#         dimacs+=f"-{somColor[l[1:]]}"
#     else:
#         dimacs+=f"-{somColor[l]}"
#     dimacs+="0\n"
# print(dimacs)
#python tp2.py > tp2.cnf



print()
for c in clauses:
    print(c)

open('colorer.cnf', 'w').close()

with open("colorer.cnf","a") as f:
    f.write("c exercice COLORER\np cnf 9 21\n")
    for clause in clauses:
        prompt=""
        for l in clause:
            print(l)
            if l[0] == '-':
                prompt+= '-'+str((somColor[l[1:]]+1))
            else:
                prompt+= str(somColor[l]+1)
            prompt+=" "
        prompt+="0\n"
        f.write(prompt)

        
    