from typing import Generator, List


def decomp(n: int, nb_bits: int) -> list[bool]:
    """decompose un nombre n de base 10 en base 2 sur nb_bits bits,
    en divisant successivement par 2."""
    bits = []
    while n > 0:
        bits.append(n % 2 == 1)
        n //= 2
    while len(bits) < nb_bits:
        bits.append(False)
    return bits


def interpretation(voc: list[str], vals: list[bool]) -> dict[str, bool]:
    if len(voc) != len(vals):
        raise ValueError("Les deux arguments doivent etre de meme longuers.")

    dico: dict[str, bool] = {}
    for i in range(len(voc)):
        dico[voc[i]] = vals[i]
    return dico


def gen_interpretations(voc: list[str]) -> Generator[dict[str, bool], None, None]:
    i = 0
    while i < 2 ** len(voc):
        # print(len(voc), len(decomp(i,len(voc))))
        yield interpretation(voc, decomp(i, len(voc)))
        i += 1


# def my_range(n: int):
#     i = 0
#     while i < n:
#         yield i
#         i += 1


def valuate(formula: str, interpretation: dict[str, bool]) -> bool:
    """evalue la formule avec les valeurs de verite pour chaque variable dans la formule"""
    # evalue une chaine de caractere qui represente une expression
    # les valeurs sont a remplacees par celle dans le dico
    return eval(formula, interpretation)


def table(formule: str, vocab: list[str]) -> None:
    """affiche une jolie table"""
    ligne = "+" + "---+" * len(vocab) + "-------+"

    # en-tete
    print(f"formule : {formule}")
    print(ligne)
    print("|", end='')
    for v in vocab:
        print(f" {v} |", end="")
    print(" eval. |")
    print(ligne)

    # corps
    for interpretation in gen_interpretations(vocab):
        print("|", end='')
        for val in interpretation.values():
            print(" T |", end='') if val else print(" F |", end='')
        res = valuate(formule, interpretation)
        print("   T   |", end='') if res else print("   F   |", end='')
        print()
    print(ligne)


def valide(formula: str, voc: List[str]) -> bool:
    """la formule est toujours vraie"""
    for interpretation in gen_interpretations(voc):
        if not valuate(formula, interpretation):
            return False
    return True


def contradictoire(formula: str, voc: List[str]) -> bool:
    """la formule est toujours fausse"""
    for interpretation in gen_interpretations(voc):
        if valuate(formula, interpretation):
            return False
    return True


def contingente(formula: str, voc: List[str]) -> bool:
    """la formule est soit vrais, soit faux"""
    return not valide(formula, voc) and not contradictoire(formula, voc)


def is_cons(f1: str, f2: str, voc: List[str]) -> bool:
    """si f1 est vraie, forcement f2 est vraie aussi"""
    for interpretation in gen_interpretations(voc):
        if valuate(f1, interpretation) and not valuate(f2, interpretation):
            return False
    return True


def main():
    # print(decomp(7,3))
    # interpretation(["A", "B", "C"],[True, True, False])

    # ran=my_range(5)
    # print(next(ran))
    # print(next(ran))

    # for i in gen_interpretations(["toto", "tutu"]):
    #     print(i)

    # g = gen_interpretations(["A", "B", "C"])
    # for i in g:
    #     print(i)

    # valuate("(A or B) and not(C)", next(g))

    # print(valuate("(A or B) and not(C)", {"A": True, "B": False, "C": False}))

    # table("(A or B) and not(C) or D", ["A", "B", "C", 'D'])

    # TEST Q6: valide/contradictoire/contigent
    # print(contingente("(A or B) and not(C)", ["A", "B", "C"]))
    # print(valide("A or not A", ["A"]))
    # print(contradictoire("A and not A", ["A"]))

    # print(valide("x1 or not x1",[f"x{i}" for i in range(20)]))
    # prend beaucoup plus de temps que si on donnait juste 1 variable

    pass


if __name__ == "__main__":
    main()
    # print("Hello World!")
