import ast
from typing import Callable
import random
import math
import itertools

# from pprint import pprint

Grid = tuple[tuple[int, ...], ...]  # eg: ((X,O,X),(X,X,O),(O,X,X))
State = Grid  # un etat du jeu
Action = tuple[int, int]  # eg: (0,1)
Player = int  # eg: X,O
Score = float

Strategy = Callable[[State, Player], Action]  # pb

# Quelques constantes
DRAW = 0
EMPTY = 0
X = 1
O = 2

EMPTY_GRID: Grid = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
GRID_0: Grid = EMPTY_GRID
GRID_1: Grid = ((0, 0, 0), (0, X, O), (0, 0, 0))
# (0, 0, 0),
# (0, X, O),
# (0, 0, 0))

GRID_2: Grid = ((O, 0, X), (X, X, O), (O, X, 0))
# ((O, 0, X),
# (X, X, O),
# (O, X, 0))

GRID_3: Grid = ((O, 0, X), (0, X, O), (O, X, 0))
# ((O, 0, X),
# (0, X, O),
# (O, X, 0))

GRID_4: Grid = ((0, 0, 0), (X, X, O), (0, 0, 0))
# ((0, 0, 0),
# (X, X, O),
# (0, 0, 0))

GRID_5: Grid = ((X, 0, 0), (X, X, O), (0, 0, X))
# ((0, 0, 0),
# (X, X, O),
# (0, 0, 0))

GRID_6: Grid = ((X, O, O), (X, 0, O), (X, 0, X))


def grid_tuple_to_grid_list(grid: Grid) -> list[list[int]]:
    return list(list(i) for i in grid)  # map(list(grid))


def grid_list_to_grid_tuple(grid: list[list[int]]) -> Grid:
    return tuple(tuple(i) for i in grid)
    # tuple(itertools.imap(tuple,grid))


def legals(grid: State) -> list[Action]:
    actions = []
    for i in range(3):
        for j in range(3):
            if grid[i][j] == EMPTY:
                actions.append((i, j))

    return actions


# print(legals(GRID_0))


def diagonal(grid: State, player: Player) -> bool:
    return grid[0][0] == grid[1][1] == grid[2][2] == player


def anti_diagonal(grid: State, player: Player) -> bool:
    return grid[0][2] == grid[1][1] == grid[2][0] == player


def line(grid: State, player: Player) -> bool:
    # verif lignes
    ligne = (player, player, player)
    if any(row == ligne for row in grid):
        return True

    # verif col
    for i in range(3):
        # if all(grid[j][i] == player for j in range(3)):
        if grid[0][i] == grid[1][i] == grid[2][i] == player:
            return True

    return diagonal(grid, player) or anti_diagonal(grid, player)

    return False


# print(line(GRID_5, X))

def final(grid: State) -> bool:
    """si on est dans un etat terminal : gain ou plus de cases vides"""
    return line(grid, X) or line(grid, O) or len(legals(grid)) == 0


# print(final(GRID_6))

def score(grid: State) -> Score:
    """
    en supposant que le score est à donner pour X.
    alors, si c'est O qui forme une ligne, alors on affiche -1
    """
    if line(grid, X):
        return 1
    if line(grid, O):
        return -1
    return 0


def pprint(grid: State):
    """affichage de la grille de jeu"""
    for row in grid:
        for cell in row:
            if cell in (EMPTY, 0):
                print('.', end=" ")
            elif cell in (X, 1):
                print("X", end=" ")
            elif cell in (O, 2):
                print("O", end=" ")
        print()


# pprint(GRID_6)
# pprint(GRID_3)


# def pprint(grid: State):
#     for i in range(3):
#         for j in range(3):
#             if grid[i][j] == X:
#                 print("X", end=" ")
#             elif grid[i][j] == O:
#                 print("O", end=" ")
#             else:
#                 print(".", end=" ")
#         print()


def play(grid: State, player: Player, action: Action) -> State:
    """met a jour la grille avec l'action du joueur"""
    if action not in legals(grid):
        return grid

    g = grid_tuple_to_grid_list(grid)
    g[action[0]][action[1]] = player

    return grid_list_to_grid_tuple(g)


# UNE STRATEGIE RENVOIE L ACTION CHOISIE PAR LE JOUEUR

def strategy_brain(grid: State, player: Player) -> Action:
    """renvoie le tuple (action) saisi par le player"""
    player_str = "X" if player == X else "O"
    print(f"\nA vous de jouer, placez un {player_str} sur une case (x,y) : ", end="")
    s = input()  # eg: (0,2)
    print()
    t = ast.literal_eval(s)  # arbre syntaxique abstrait
    # evaluer la chaine et le convertit en obj python correspondant

    return t  # un tuple (0,2)


def tictactoe(strategy_X: Strategy, strategy_O: Strategy, debug: bool = False) -> Score:
    """boucle du jeu jusqu'a determiner le gagnant et le score"""
    g = EMPTY_GRID
    if debug:
        pprint(g)

    current_player = X
    strategies = {X: strategy_X, O: strategy_O}

    while not final(g):
        # Joueur courant joue
        action = strategies[current_player](g, current_player)
        g = play(g, current_player, action)
        if debug:
            pprint(g)

        # Test si fin
        if line(g, current_player):
            if debug:
                player_str = "X" if current_player == X else "O"
                print(f"Fin du jeu ! Le joueur {player_str} gagne.")
            return score(g)

        current_player = O if current_player == X else X

    if debug:
        print("Match nul !")
    return score(g)


# tictactoe(strategy_brain, strategy_brain, debug=True)


def strategy_first_legal(grid: State, player: Player) -> Action:
    return legals(grid)[0]


def strategy_random(grid: State, player: Player) -> Action:
    actions = legals(grid)
    i = random.randrange(0, len(actions))  # random.randint (borne incluse), mais randrange exclu borne
    return actions[i]
    # return random.choices(actions)


### MIN MAX ###


def minmax(grid: State, player: Player) -> Score:
    """avec l'etat courant du jeu, donne le meilleur score possible"""
    if final(grid):
        return score(grid)

    if player == X:  # X, maximizing player
        value = -math.inf
        for action in legals(grid):
            g = play(grid, X, action)
            value = max(value, minmax(g, O))
        return value
    else:  # O, minimizing player
        value = math.inf
        for action in legals(grid):
            g = play(grid, O, action)
            value = min(value, minmax(g, X))
        return value


# print((minmax(GRID_0,X))) # match nul si joeurs normaux
# print((minmax(GRID_6, O)))  # oui, gain pour X : res = 1


def minmax_depth(grid: State, player: Player, depth=9) -> Score:
    """avec l'etat courant du jeu, donne le meilleur score possible, en limitant la profondeur de recherche"""
    if depth == 0 or final(grid):
        return score(grid)

    if player == X:  # X, maximizing player
        value = -math.inf
        for action in legals(grid):
            g = play(grid, X, action)
            value = max(value, minmax_depth(g, O, depth - 1))
        return value
    else:  # O, minimizing player
        value = math.inf
        for action in legals(grid):
            g = play(grid, O, action)
            value = min(value, minmax_depth(g, X, depth - 1))
        return value


# print(minmax_depth(GRID_0, O, depth=3))
# print(minmax_depth(GRID_6, X, depth=3)) # meme resultat que minmax mais + rapide

# TODO !!
def evaluation(grid: State, player: Player) -> Score:
    """pre """
    pass


def minmax_eval(grid: State, player: Player, depth=9) -> Score:
    """
    fonction d'évaluation: au lieu d'appeler score(), on evalue l'état pour estimer sa veleur
    """
    if depth == 0 or final(grid):
        return evaluation(grid, player)  # Utilise la fonction d’évaluation

    if player == X:  # Maximizing
        value = -math.inf
        for action in legals(grid):
            g = play(grid, X, action)
            value = max(value, minmax_eval(g, O, depth-1))
        return value
    else:  # Minimizing
        value = math.inf
        for action in legals(grid):
            g = play(grid, O, action)
            value = min(value, minmax_eval(g, X, depth-1))
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

# print(minmax_action(m, X, 4))
