from typing import Generator, List


def decomp(n: int, nb_bits: int) -> list[bool]:
    """Decompose un nombre n de base 10 en base 2 sur nb_bits bits,
    en divisant successivement par 2."""
    bits = []
    while n > 0:
        bits.append(n % 2 == 1)
        n //= 2
    while len(bits) < nb_bits:
        bits.append(False)
    return bits


def interpretation(voc: list[str], vals: list[bool]) -> dict[str, bool]:
    """Renvoie un dictionnaire associant chaque variable à une valeur de vérité"""
    if len(voc) != len(vals):
        raise ValueError("Les deux arguments doivent entre de meme longueurs.")

    dico: dict[str, bool] = {}
    for i in range(len(voc)):
        dico[voc[i]] = vals[i]
    return dico


def gen_interpretations(voc: list[str]) -> Generator[dict[str, bool], None, None]:
    """Génère toutes les interprétations possibles pour l'ensemble du vocabulaire"""
    i = 0
    while i < 2 ** len(voc):
        yield interpretation(voc, decomp(i, len(voc)))
        i += 1


def valuate(formula: str, interpretation: dict[str, bool]) -> bool:
    """Value la formule avec les valeurs de verite pour chaque variable dans la formule"""
    return eval(formula, interpretation)


def table(formule: str, vocab: list[str]) -> None:
    """Affiche une jolie table"""
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
    """La formule est toujours vraie"""
    for interpretation in gen_interpretations(voc):
        if not valuate(formula, interpretation):
            return False
    return True


def contradictoire(formula: str, voc: List[str]) -> bool:
    """La formule est toujours fausse"""
    for interpretation in gen_interpretations(voc):
        if valuate(formula, interpretation):
            return False
    return True


def contingente(formula: str, voc: List[str]) -> bool:
    """La formule est soit vrais, soit faux"""
    return not valide(formula, voc) and not contradictoire(formula, voc)


def is_cons(f1: str, f2: str, voc: List[str]) -> bool:
    """Si f1 est vraie, forcement f2 est vraie aussi"""
    for interpretation in gen_interpretations(voc):
        if valuate(f1, interpretation) and not valuate(f2, interpretation):
            return False
    return True


def main():
    print("=== Table de vérité ===")
    try:
        formule = input("Saisir une formule logique (ex : A and not B or C) : ").strip()
        vocab_str = input("Saisir les variables séparées par des virgules (ex : A,B,C) : ").strip()
        vocab = [v.strip() for v in vocab_str.split(",") if v.strip()]
        if not formule or not vocab:
            print("Erreur : formule ou vocabulaire vide.")
            return
        table(formule, vocab)
        print()
        print("La formule est :")
        if valide(formule, vocab):
            print("  - valide (tautologie)")
        elif contradictoire(formule, vocab):
            print("  - contradictoire (toujours fausse)")
        else:
            print("  - contingente (ni toujours vraie ni toujours fausse)")
    except (SyntaxError, NameError, TypeError, ValueError) as e:
        print(f"Erreur de saisie ou d'évaluation : {e}")


if __name__ == "__main__":
    main()
