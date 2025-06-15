from typing import Callable
import random
import math
import itertools

Grid = tuple[tuple[int, ...], ...]
State = Grid
Action = tuple[int, int]
Player = int
Score = float

Strategy = Callable[[State, Player], Action]  # pb

# Quelques constantes
DRAW = 0
EMPTY = 0
X = 1
O = 2


def grid_tuple_to_grid_list(grid: Grid) -> list[list[int]]:
    return list(list(i) for i in grid)  # map(list(grid))


def grid_list_to_grid_tuple(grid: list[list[int]]) -> Grid:
    return tuple(tuple(i) for i in grid)
    # tuple(itertools.imap(tuple,grid))


def legals(grid: State) -> list[Action]:
    if type(grid) != Grid:
        g = grid_tuple_to_grid_list(grid)
    else:
        g = grid

    # compter le nombre de X et O pour savoir cest a qui de jouer
    # nbO=nbX=0
    # current = 0
    actions = []

    # for line in g:
    #     for cell in line:
    #         if cell == 1:
    #             X+=1
    #         elif cell==2:
    #             O+=1
    # if nbO==nbX:
    #     current=1
    #     print("Voici les actions qui s'offrent à X : ")
    # else:
    #     current=2
    #     print("Voici les actions qui s'offrent à O : ")

    for i in range(3):
        for j in range(3):
            if g[i][j] == EMPTY:
                actions.append((i, j))

    return actions


def diagonal(grid: State, player: Player) -> bool:
    return grid[0][0] == grid[1][1] == grid[2][2] == player


def anti_diagonal(grid: State, player: Player) -> bool:
    return grid[0][2] == grid[1][1] == grid[2][0] == player


def line(grid: State, player: Player) -> bool:
    # TODO: mettre un Flag pour ne pas avoir tout parcourir

    g = grid_list_to_grid_tuple(grid)

    # verif lignes
    ligne = (player, player, player)
    for row in g:
        if row == ligne:
            return True

    # verif col
    for i in range(3):
        if g[0][i] == g[1][i] == g[2][i] == player:
            return True

    return diagonal(g, player) or anti_diagonal(g, player)

    return False


def final(grid: State) -> bool:
    # for row in grid:
    #     for cell in row:
    #         if cell is EMPTY:
    #             return False

    # return True

    return line(grid, X) or line(grid, O) or len(legals(grid)) == 0


def score(grid: State) -> Score:
    """en supposant que le score est à donner pour X.
    alors, si c'est O qui forme une ligne, alors on affiche -1
    """

    if line(grid, X):
        return 1
    if line(grid, O):
        return -1
    return 0


## TODO : a revoir pourquoi ca ne marche pas
# def pprint(grid: State):
#     """affichage de la grille de jeu"""
#     for row in grid:
#         for cell in grid:
#             if cell[0] == EMPTY or cell[0] == 0:
#                 print('.', end=" ")
#             elif cell[0] == X or cell == 1:
#                 print("X", end= " ")
#             elif cell[0] == O or cell == 2:
#                 print("O", end= " ")
#         print()


def pprint(grid: State):
    for i in range(3):
        for j in range(3):
            if grid[i][j] == X:
                print("X", end=" ")
            elif grid[i][j] == O:
                print("O", end=" ")
            else:
                print(".", end=" ")
        print()


def play(grid: State, player: Player, action: Action) -> State:
    if action not in legals(grid):
        return grid

    g = grid_tuple_to_grid_list(grid)
    g[action[0]][action[1]] = player

    return grid_list_to_grid_tuple(g)


# def play(grid: State, player: Player, action: Action) -> State:
#     g=[list(l) for l in grid]
#     g[action[0]][action[1]]=player
#     return tuple(map(tuple,g))


def strategy_brain(grid: State, player: Player) -> Action:
    print("à vous de jouer: ", end="")
    s = input()
    print()
    t = ast.literal_eval(s)

    return t


def tictactoe(strategy_X: Strategy, strategy_O: Strategy, debug: bool = False) -> Score:
    g = ((0, 0, 0), (0, 0, 0), (0, 0, 0))

    while not final(g):
        action = strategy_X(g, X)
        g = play(g, X, action)

        action = strategy_O(g, O)
        g = play(g, O, action)

        if line(g, X) or line(g, O):
            return score(g)


def strategy_first_legal(grid: State, player: Player) -> Action:
    return legals(grid)[0]


def strategy_random(grid: State, player: Player) -> Action:
    actions = legals(grid)
    i = random.randrange(0, len(actions))
    return actions[i]
    # return random.choices(actions)


# IMPLEMENTATION MIN MAX


##TODO: tester
def minmax(grid: State, player: Player) -> Score:
    if final(grid):
        return score(grid)

    if player == X:  # X, maximizing Player
        value = -math.inf
        for etat in legals(grid):
            value = max(value, minmax(etat, O))
        return value

    else:  # O, minimizing Player
        value = math.inf
        for etat in legals(grid):
            value = max(value, minmax(etat, X))
        return value


# https://papers-100-lines.medium.com/the-minimax-algorithm-and-alpha-beta-pruning-tutorial-in-30-lines-of-python-code-e4a3d97fa144
def minmax_action(grid: State, player: Player, depth: int = 0) -> tuple[Score, Action]:
    # action: tuple[int,int] = None
    if depth == 0 or final(grid):
        return score(grid), (-1, -1)

    if player == X:  # X, maximizing Player
        value = -math.inf
        for action in legals(grid):
            v = minmax_action(action, O, depth - 1)[0]  # on prend le score du retour
            if v > value:
                bestAction = action
                value = v
        return value, bestAction

    else:  # O, minimizing Player
        value = math.inf
        for action in legals(grid):
            v = minmax_action(action, X, depth - 1)[0]  # on prend le score du retour
            if v > value:
                bestAction = action
                value = v
        return value, bestAction


# TODO : quelle depth par defaut choisir?
def strategy_minmax(grid: State, player: Player) -> Action:
    return minmax_action(grid, player, 5)[0]


def minmax_actions(
    grid: State, player: Player, depth: int = 0
) -> tuple[Score, list[Action]]:
    # action: tuple[int,int] = None
    actions = []
    if depth == 0 or final(grid):
        return score(grid), []

    if player == X:  # X, maximizing Player
        value = -math.inf
        for action in legals(grid):
            v = minmax_action(action, O, depth - 1)[0]  # on prend le score du retour
            if v > value:
                actions.append(action)
                value = v
        return value, actions

    else:  # O, minimizing Player
        value = math.inf
        for action in legals(grid):
            v = minmax_action(action, X, depth - 1)[0]  # on prend le score du retour
            if v > value:
                actions.append(action)
                value = v
        return value, actions


# TODO : cest quoi minmax indeterministe ??
def strategy_minmax_random(grid: State, player: Player) -> Action:
    pass


# TODO : ajout cache


# alpha beta
def alphabeta(grid: State, player: Player, alpha=-math.inf, beta=math.inf) -> Score:
    if final(grid):
        return score(grid)

    if player == X:  # X, maximizing Player
        value = -math.inf
        for action in legals(grid):  # liste d'actions !! ensuite faut les jouer
            g = play(grid, player, action)
            value = max(value, alphabeta(g, alpha, beta, O))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value

    else:  # O, minimizing Player
        for action in legals(grid):  # liste d'actions !! ensuite faut les jouer
            g = play(grid, player, action)
            value = min(value, alphabeta(g, alpha, beta, X))
            alpha = min(alpha, value)
            if alpha >= beta:
                break
        return value


# TODO bonue: alpha beta avec depth


# TESTS ====
m = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
g = ((1, 1, 1), (0, 0, 0), (0, 0, 0))
h = ((X, 0, 0), (0, X, 0), (0, 0, X))  # X win
k = ((0, X, 0), (0, X, O), (0, X, 0))
r = ((O, X, X), (O, O, X), (X, X, O))

# for r in g:
#     for l in g:
#         print (type(l[0]))

# print(type(X))


# g2 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

g1 = ((0, 0, 0), (0, X, O), (0, 0, 0))
# (0, 0, 0),
# (0, X, O),
# (0, 0, 0))

g2 = ((O, 0, X), (X, X, O), (O, X, 0))
# ((O, 0, X),
# (X, X, O),
# (O, X, 0)

g3 = ((O, 0, X), (0, X, O), (O, X, 0))
# ((O, 0, X),
# (0, X, O),
# (O, X, 0))

g4 = ((0, 0, 0), (X, X, O), (0, 0, 0))
# ((0, 0, 0),
# (X, X, O),
# (0, 0, 0))


# print(grid_tuple_to_grid_list(g))
# print(grid_list_to_grid_tuple(g2))
# print(legals(g))
# print(line(k,X))
# print(final(g))
# print(score(r))

# pprint(r)

# pprint(h)
# pprint(play(h,O,(1,0)))

# print(strategy_first_legal(g4,O))

# print(strategy_random(g4,O))

# print(tictactoe(strategy_random, strategy_random))

# print(minmax(m, X))  #!! ERROR

print(minmax_action(m, X, 4))
