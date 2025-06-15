"""
[IA02] TP SAT/Sudoku template python
author:  Sylvain Lagrue
version: 1.1.0
"""

from typing import List, Tuple
import subprocess
from itertools import combinations


# alias de types
Grid = List[List[int]] 
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]

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

# fonctions utilitaires

#attention, les (i,j) sont numerotes à partir de 0
def cell_to_variable(i: int, j: int, val: int) -> PropositionnalVariable:
    """to check"""
    return (9*j+val)+i*9*9+1

# print(cell_to_variable(2,1,1))

def variable_to_cell(var: PropositionnalVariable) -> Tuple[int, int, int]:
    """ to do"""
    i=var//81-1
    j=(var-9*i+1)//9
    v=j

    return i,j,v

# print(729//81)
# print(variable_to_cell(1))

def model_to_grid(model: Model, nb_vals: int = 9) -> Grid:
    """cor"""
    grid=[[0 for i in range((9))]for j in range(9)] 
    for lit in model:
        if lit>0:
            i,j,v=variable_to_cell(lit)
            grid[i][j]=v

    return grid

def at_least_one(variables:List[PropositionnalVariable])->Clause:
    return variables

def unique(variables: List[PropositionnalVariable]) -> ClauseBase:
    liste = [at_least_one(variables)]
    for v1,v2 in combinations(variables,2):
        liste.append([-v1,-v2])
    return liste

# print(unique([1, 3, 5]))

def create_cell_constraints() -> ClauseBase:
    clauses=[]
    for i in range(0,nb_vals):
        for j in range(0,nb_vals):
            clauses+=unique([cell_to_variable(i,j,v) for v in range(1,nb_vals+1)])
    return clauses


def create_line_constraints() -> ClauseBase:
    pass

def create_column_constraints() -> ClauseBase:
    pass

def create_box_constraints() -> ClauseBase:
    """cf photo"""
    
    pass

def create_value_constraints(grid: Grid) -> ClauseBase:
    pass

def generate_problem(grid: Grid) -> ClauseBase:
    pass

def clauses_to_dimacs(clauses: ClauseBase, nb_vars: int) -> str:
    pass

#### fonctions fournies
def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)


def exec_gophersat(
    filename: str, cmd: str = "gophersat", encoding: str = "utf8"
) -> Tuple[bool, List[int]]:
    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:-2].split(" ")

    return True, [int(x) for x in model]


#### fonction principale


# def main():
#     pass


# if __name__ == "__main__":
#     main()
