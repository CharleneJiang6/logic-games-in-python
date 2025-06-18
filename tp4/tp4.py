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

GRID_6: Grid = ((X, O, O), (O, 0, O), (X, 0, X))


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


def next_player(player: Player) -> Player:
    if player == X:
        return O
    return X


####################### MIN MAX ##########################


# def memoize(
#         f: Callable[[State, Player], tuple[Score, Action]]
# ) -> Callable[[State, Player], tuple[Score, Action]]:
#     cache = {}  # closure
#
#     def g(state: State, player: Player):
#         if state in cache:
#             return cache[state]
#
#         val = f(state, player)
#         cache[state] = val
#         return val
#
#     return g


def memoize(f: Callable) -> Callable:
    cache = {}

    def g(*args):
        if args in cache:
            return cache[args]
        val = f(*args)
        cache[args] = val
        return val

    return g


def symetries(grid: Grid) -> list[Grid]:
    """grilles symétriques (rotations et miroirs)"""
    grids = []
    g = grid
    for _ in range(4):  # 4 rotations (0°, 90°, 180°, 270°)
        grids.append(g)
        grids.append(tuple(row[::-1] for row in g))  # miroir horizontal
        # Rotation de 90°
        g = tuple(zip(*g[::-1]))
    return grids


def min_sym(grid):
    return min(symetries(grid))


def memoize_symmetry(f):
    cache = {}

    def g(grid, *args):
        key = (min_sym(grid),) + args
        if key in cache:
            return cache[key]
        val = f(grid, *args)
        cache[key] = val
        return val

    return g


def evaluation(grid: State, player: Player) -> Score:
    adversaire = 'O' if player == 'X' else 'X'

    # Si le joueur courant gagne
    if line(grid, player):
        return 100
    # Si l’adversaire gagne
    if line(grid, adversaire):
        return -100
    return 0


@memoize
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

@memoize
def alphabeta(grid: State, player: Player, alpha: Score, beta: Score) -> Score:
    """avec l'etat courant du jeu, donne le meilleur score possible"""
    if final(grid):
        return score(grid)

    if player == X:  # Maximizing player
        value = -math.inf
        for action in legals(grid):
            g = play(grid, X, action)
            value = max(value, alphabeta(g, O, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta cut
        return value
    else:  # Minimizing player
        value = math.inf
        for action in legals(grid):
            g = play(grid, O, action)
            value = min(value, alphabeta(g, X, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break  # alpha cut
        return value


# print(alphabeta(EMPTY_GRID, X, -math.inf, math.inf))

@memoize
def minmax_depth(grid: State, player: Player, depth=9) -> Score:
    """avec l'etat courant du jeu, donne le meilleur score possible, en limitant la profondeur de recherche"""
    if depth == 0 or final(grid):
        return score(grid)  # ou evaluation

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

@memoize
def alphabeta_depth(grid: State, player: Player, alpha: Score, beta: Score, depth=9) -> Score:
    """avec l'etat courant du jeu, donne le meilleur score possible"""
    if depth == 0 or final(grid):
        return score(grid)

    if player == X:  # Maximizing player
        value = -math.inf
        for action in legals(grid):
            g = play(grid, X, action)
            value = max(value, alphabeta_depth(g, O, alpha, beta, depth - 1))
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta cut
        return value
    else:  # Minimizing player
        value = math.inf
        for action in legals(grid):
            g = play(grid, O, action)
            value = min(value, alphabeta_depth(g, X, alpha, beta, depth - 1))
            beta = min(beta, value)
            if alpha >= beta:
                break  # alpha cut
        return value


# print(alphabeta_depth(EMPTY_GRID, X, -math.inf, math.inf, 5))


@memoize
def minmax_eval(grid: State, player: Player, depth: int = 9) -> Score:
    """
    fonction d'évaluation : au lieu d'appeler score(), on evalue l'état pour estimer sa veleur
    """
    if depth == 0 or final(grid):
        return evaluation(grid, player)  # Utilise la fonction d’évaluation

    if player == X:  # Maximizing
        value = -math.inf
        for action in legals(grid):
            g = play(grid, X, action)
            value = max(value, minmax_eval(g, O, depth - 1))
        return value
    else:  # Minimizing
        value = math.inf
        for action in legals(grid):
            g = play(grid, O, action)
            value = min(value, minmax_eval(g, X, depth - 1))
        return value


@memoize
def minmax_action(grid: State, player: Player, depth: int = 9) -> tuple[Score, Action]:
    """en plus du score optimal, donne l'action qui a permis d'y parvenir"""

    if depth == 0 or final(grid):
        return score(grid), (-1, -1)

    best_action: tuple[int, int] = (-1, -1)

    if player == X:  # X, maximizing Player
        value = -math.inf
        for action in legals(grid):
            g = play(grid, X, action)
            v = minmax_action(g, O, depth - 1)[0]  # on prend le score du retour
            if v > value:
                best_action = action
                value = v
        return value, best_action

    else:  # O, minimizing Player
        value = math.inf
        for action in legals(grid):
            g = play(grid, O, action)
            v = minmax_action(g, X, depth - 1)[0]  # on prend le score du retour
            if v < value:  # on veut petite valeur
                best_action = action
                value = v
        return value, best_action


# pprint(GRID_6)
# print(minmax_action(GRID_6, O))
# pprint(GRID_2)
# print(minmax_action(GRID_2, X))


def strategy_minmax(grid: State, player: Player) -> Action:
    """retourne l'action qui permet d'arriver au score optimal"""
    return minmax_action(grid, player)[1]


@memoize
def alphabeta_action(
        grid: State, player: Player, depth: int = 9, alpha: float = -math.inf, beta: float = math.inf
) -> tuple[Score, Action]:
    """retourne score optimal et action qui y mène"""

    if depth == 0 or final(grid):
        return score(grid), (-1, -1)

    best_action = (-1, -1)

    if player == X:  # Maximizing
        value = -math.inf
        for action in legals(grid):
            g = play(grid, X, action)
            v, _ = alphabeta_action(g, O, depth - 1, alpha, beta)
            if v > value:
                value = v
                best_action = action
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_action

    else:  # Minimizing
        value = math.inf
        for action in legals(grid):
            g = play(grid, O, action)
            v, _ = alphabeta_action(g, X, depth - 1, alpha, beta)
            if v < value:
                value = v
                best_action = action
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value, best_action


# print(alphabeta_action(EMPTY_GRID,X))

def strategy_alphabeta(grid: State, player: Player) -> Action:
    """retourne l'action qui permet d'arriver au score optimal"""
    return alphabeta_action(grid, player)[1]


@memoize
def minmax_actions(grid: State, player: Player, depth: int = 9) -> tuple[Score, list[Action]]:
    """renvoie le score optimal et la liste des actions menant a ce score optimal"""
    if final(grid) or depth == 0:
        return score(grid), []

    actions: list[Action] = legals(grid)
    best_score: float = None
    best_actions: list[Action] = []

    if player == X:  # maximizing
        best_score = -math.inf
        for action in actions:
            g = play(grid, X, action)
            v, _ = minmax_actions(g, O, depth - 1)
            if v > best_score:
                best_score = v  # mettre a jour la meilleure valeur
                best_actions = [action]
            elif v == best_score:
                best_actions.append(action)
        return best_score, best_actions

    else:  # minimizing
        best_score = math.inf
        for action in actions:
            g = play(grid, O, action)
            v, _ = minmax_actions(g, X, depth - 1)
            if v < best_score:
                best_score = v
                best_actions = [action]
            elif v == best_score:
                best_actions.append(action)
        return best_score, best_actions


# pprint(EMPTY_GRID)
# print(minmax_actions(EMPTY_GRID, player=X)) # toutes les positions sont optimales
# pprint(GRID_6)
# print(minmax_actions(GRID_6, player=X)) # toutes les positions sont optimales


def strategy_minmax_random(grid: State, player: Player) -> Action:
    """minmax indeterministe : choisit aleatoirement parmi les actions optimales"""
    _, actions = minmax_actions(grid, player)
    if not actions:
        return (-1, -1)  # aucun coup possible
    return random.choice(actions)


# print(strategy_minmax_random(EMPTY_GRID, X))

@memoize
def alphabeta_actions(
        grid: State,
        player: Player,
        depth: int = 9,
        alpha: float = -math.inf,
        beta: float = math.inf
) -> tuple[Score, list[Action]]:
    """renvoie le score optimal et la liste des actions menant à ce score optimal, avec élagage alpha-bêta."""
    if final(grid) or depth == 0:
        return score(grid), []

    actions = legals(grid)
    best_actions = []

    if player == X:  # Maximizing
        best_score = -math.inf
        for action in actions:
            g = play(grid, X, action)
            v, _ = alphabeta_actions(g, O, depth - 1, alpha, beta)
            if v > best_score:
                best_score = v
                best_actions = [action]
            elif v == best_score:
                best_actions.append(action)
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break  # Beta cut-off
        return best_score, best_actions

    else:  # Minimizing
        best_score = math.inf
        for action in actions:
            g = play(grid, O, action)
            v, _ = alphabeta_actions(g, X, depth - 1, alpha, beta)
            if v < best_score:
                best_score = v
                best_actions = [action]
            elif v == best_score:
                best_actions.append(action)
            beta = min(beta, best_score)
            if beta <= alpha:
                break  # Alpha cut-off
        return best_score, best_actions


def strategy_alphabeta_random(grid: State, player: Player) -> Action:
    """alphabeta indeterministe : choisit aleatoirement parmi les actions optimales"""
    _, actions = alphabeta_actions(grid, player)
    if not actions:
        return (-1, -1)  # aucun coup possible
    return random.choice(actions)


tictactoe(strategy_alphabeta_random, strategy_first_legal, True)

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
