from typing import *

def decomp(n: int, nb_bits: int) -> list[bool]:
    counter = 0
    l = list()

    while n>0:
        # print(n%2==1, end=' ')
        l.append(n%2==1)
        n//=2
        counter+=1
    
    while counter<nb_bits:
        # print("False", end=' ')
        counter+=1
        l.append(False)
    
    return l

def interpretation(voc: list[str], vals: list[bool]) -> dict[str, bool]:
    dico={}
    for i in range (len(voc)):
        dico[voc[i]]=vals[i]
    return(dico)


def gen_interpretations(voc: list[str]) -> Generator[dict[str, bool], None, None]:
    i=0
    while i<pow(len(voc),2):
        yield interpretation(voc, list(decomp(i, len(voc))))
        i+=1

def my_range(n:int):
    i=0
    while i<n:
        yield i
        i+=1

def valuate(formula: str, interpretation: dict[str, bool]) -> bool:
        return eval(formula,interpretation)


def table(formule: str, voc: list[str]):
    # utiliser gen_inter que l'on va evaluer
    n=len(voc)

    print("+",end='')
    for i in range (n):
        print("---+", end='')
    print("------+")

    # print 2e ligne

    for i in gen_interpretations(voc):
        print(i, end=' ')
        print(valuate(formule, i))

    
    


def main():
    # print(decomp(7,3))
    # interpretation(["A", "B", "C"],[True, True, False])
    
    # ran=my_range(5)
    # print(next(ran))
    # print(next(ran))

    # for i in gen_interpretations(["toto", "tutu"]):
    #     i

    # g = gen_interpretations(["A", "B", "C"])
    # print(type(next(g)))

    #valuate("(A or B) and not(C)", next(g))
    # print(next(g))

    #valuate("(A or B) and not(C)", {"A": True, "B": False, "C": False})

    table("(A or B) and not(C)", ["A", "B", "C"])
    




if __name__=="__main__":
    main()