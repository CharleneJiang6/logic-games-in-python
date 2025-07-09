from typing import List, Tuple, Any  # type: ignore
import subprocess
from itertools import combinations
import math

Grid = List[List[int]]
PropositionnalVariable = int  # eg: 1
Literal = int  # eg: -1
Clause = List[Literal]  # eg: [-1, 3, 5]
ClauseBase = List[Clause]  # eg:[[-1, 3, 5], [-2, 3, 6]]
Model = List[Literal]  # assignation de verite qui rend la formule vraie
nb_vals = 9

example: Grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

example2: Grid = [
    [0, 0, 0, 0, 2, 7, 5, 8, 0],
    [1, 0, 0, 0, 0, 0, 0, 4, 6],
    [0, 0, 0, 0, 0, 9, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 0, 2, 0],
    [0, 0, 0, 8, 1, 0, 0, 0, 0],
    [4, 0, 6, 3, 0, 1, 0, 0, 9],
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 2, 0, 0, 0, 0, 3, 1, 0],
]

empty_grid: Grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]


# Fonctions utilitaires

def cell_to_variable(i: int, j: int, val: int) -> PropositionnalVariable:
    """i et j sont app. [0,8] ; val app. [1,8]"""
    return i * 9 * 9 + 9 * j + val + 1


def variable_to_cell(var: PropositionnalVariable) -> Tuple[int, int, int]:
    """inverse of cell_to_variable"""
    i = (var - 1) // 81
    j = ((var - 1) // 9) % 9
    v = (var - 1) % 9

    return i, j, v


def model_to_grid(model: Model, nb_vals: int = 9) -> Grid:
    """renvoie un tab 2D représentant la grille complet"""
    grid = [[0 for i in range(nb_vals)] for j in range(nb_vals)]
    for lit in model:
        if lit > 0:
            i, j, v = variable_to_cell(lit)
            grid[i][j] = v + 1

    return grid


def at_least_one(variables: List[PropositionnalVariable]) -> Clause:
    return variables


def unique(variables: List[PropositionnalVariable]) -> ClauseBase:
    """unique = at_least_one + at_most_one"""
    clauses = [at_least_one(variables)]
    for u, v in combinations(variables, 2):
        clauses.append([-u, -v])
    return clauses


def create_cell_constraints() -> ClauseBase:
    clauses: ClauseBase = []
    # pour chaque case, recupere toutes ses variables et faire des clauses Unique
    for i in range(nb_vals):
        for j in range(nb_vals):
            clauses += unique([cell_to_variable(i, j, v) for v in range(nb_vals)])
    return clauses


def create_line_constraints() -> ClauseBase:
    clauses: ClauseBase = []
    for i in range(nb_vals):
        for v in range(nb_vals):  # pour chaque valeur 0 à 8
            variables = [cell_to_variable(i, j, v) for j in
                         range(nb_vals)]  # la valeur v apparait exactement une fois sur une ligne
            clauses += unique(variables)
    return clauses


def create_column_constraints() -> ClauseBase:
    clauses: ClauseBase = []
    for j in range(nb_vals):
        for v in range(nb_vals):
            variables = [cell_to_variable(i, j, v) for i in range(nb_vals)]
            clauses += unique(variables)
    return clauses


def create_box_constraints() -> ClauseBase:
    """un nombre apparait exactement 1x par box de 3x3"""
    clauses: ClauseBase = []
    box_size = int(math.sqrt(nb_vals))  # = 3
    # pour chaque box
    for box_i in range(box_size):
        for box_j in range(box_size):

            # pour chaque nombre, ça apparait exactement 1 fois
            for v in range(nb_vals):  # pour chaque valeur de 0 à 8
                variables: List[PropositionnalVariable] = []
                for i in range(box_i * box_size, box_i * box_size + box_size):  # parcours des lignes dans le box
                    for j in range(box_j * box_size, box_j * box_size + box_size):  # parcours des colonnes dans le box
                        variables.append(cell_to_variable(i, j, v))
                clauses += unique(variables)

    return clauses


def create_value_constraints(grid: Grid) -> ClauseBase:
    """ajouter des valeurs predefinies pour des cases"""
    clauses: ClauseBase = []

    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:  # si cest un chiffre
                clauses.append([cell_to_variable(i, j, grid[i][j] - 1)])

    return clauses


def generate_problem(grid: Grid) -> ClauseBase:
    """genere toutes les clauses pour resoudre ce probleme SAT"""
    return (create_cell_constraints() +
            create_line_constraints() +
            create_column_constraints() +
            create_box_constraints() +
            create_value_constraints(grid))


def clauses_to_dimacs(clauses: ClauseBase, nb_vars: int) -> str:
    dimacs: str = ""
    dimacs += f"p cnf {nb_vars} {len(clauses)}\n"
    for clause in clauses:
        dimacs += " ".join(map(str, clause)) + " 0\n"
    return dimacs


#### fonctions fournies
def write_dimacs_file(dimacs: str, filename: str) -> None:
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)


def print_grid(grid: Grid):
    for i in range(9):
        if i % 3 == 0:
            print("-------------------------")
        for j in range(9):
            v = grid[i][j]
            if j % 3 == 0:
                print("| ", end="")
            print(f"{v if v != 0 else '.'} ", end="")
        print("|")
    print("-------------------------")


def exec_gophersat(filename: str, cmd: str = "gophersat", encoding: str = "utf8") -> Tuple[bool, List[int]]:
    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:-2].split(" ")

    return True, [int(x) for x in model]


def resoudre(pb: Grid, fichier: str):
    dimacs_sudoku = clauses_to_dimacs(generate_problem(pb), 729)
    write_dimacs_file(dimacs_sudoku, fichier)
    verite, model_sudoku = exec_gophersat(fichier)
    solution = model_to_grid(model_sudoku)
    print_grid(solution)


def solution_unique(pb: Grid, fichier: str) -> bool:
    clauses = generate_problem(pb)
    dimacs_sudoku = clauses_to_dimacs(clauses, 729)
    write_dimacs_file(dimacs_sudoku, fichier)
    verite, model_sudoku = exec_gophersat(fichier)
    if not verite:
        return False
    clauses += [[-v for v in model_sudoku if v > 0]]
    dimacs_sudoku = clauses_to_dimacs(clauses, 729)
    write_dimacs_file(dimacs_sudoku, fichier)
    verite, model_sudoku = exec_gophersat(fichier)
    if not verite:
        return True
    return False


def main():
    # Exemple de résolution d'une grille
    resoudre(example, "sudoku/example.cnf")
    # Test d'unicité sur la grille vide
    print("Solution unique pour la grille vide ?", solution_unique(empty_grid, "sudoku/unique.cnf"))


if __name__ == "__main__":
    main()
