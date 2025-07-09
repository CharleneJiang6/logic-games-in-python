import ast
import random
import math
from typing import Callable, Tuple, List

Grid = Tuple[Tuple[int, ...], ...]  # Ex: ((X,O,X),(X,X,O),(O,X,X))
State = Grid  # Un état du jeu
Action = Tuple[int, int]  # Ex: (0,1)
Player = int  # X ou O
Score = float
Strategy = Callable[[State, Player], Action]

EMPTY = 0
X = 1
O = 2
DRAW = 0

EMPTY_GRID: Grid = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
GRID_0: Grid = EMPTY_GRID
GRID_1: Grid = ((0, 0, 0), (0, X, O), (0, 0, 0))
GRID_2: Grid = ((O, 0, X), (X, X, O), (O, X, 0))
GRID_3: Grid = ((O, 0, X), (0, X, O), (O, X, 0))
GRID_4: Grid = ((0, 0, 0), (X, X, O), (0, 0, 0))
GRID_5: Grid = ((X, 0, 0), (X, X, O), (0, 0, X))
GRID_6: Grid = ((X, O, O), (O, 0, O), (X, 0, X))


# === UTILITAIRES ===

def grid_tuple_to_grid_list(grid: Grid) -> List[List[int]]:
    return [list(row) for row in grid]


def grid_list_to_grid_tuple(grid: List[List[int]]) -> Grid:
    return tuple(tuple(row) for row in grid)


def pprint(grid: State):
    """Affiche joliment la grille."""
    for row in grid:
        for cell in row:
            if cell == EMPTY:
                print('.', end=" ")
            elif cell == X:
                print("X", end=" ")
            elif cell == O:
                print("O", end=" ")
        print()
    print()


def legals(grid: State) -> List[Action]:
    """Renvoie la liste des actions légales (cases vides)."""
    return [(i, j) for i in range(3) for j in range(3) if grid[i][j] == EMPTY]


# === CONDITIONS DE VICTOIRE ===

def diagonal(grid: State, player: Player) -> bool:
    return grid[0][0] == grid[1][1] == grid[2][2] == player


def anti_diagonal(grid: State, player: Player) -> bool:
    return grid[0][2] == grid[1][1] == grid[2][0] == player


def line(grid: State, player: Player) -> bool:
    """Test si le joueur a une ligne, colonne ou diagonale gagnante."""
    ligne = (player, player, player)
    if any(row == ligne for row in grid):
        return True
    for i in range(3):
        if grid[0][i] == grid[1][i] == grid[2][i] == player:
            return True
    return diagonal(grid, player) or anti_diagonal(grid, player)


def final(grid: State) -> bool:
    """Renvoie True si le jeu est terminé (victoire ou plus de coups possibles)."""
    return line(grid, X) or line(grid, O) or len(legals(grid)) == 0


def score(grid: State) -> Score:
    """Score final : +1 si X gagne, -1 si O gagne, 0 sinon."""
    if line(grid, X):
        return 1
    if line(grid, O):
        return -1
    return 0


# === MOTEUR DE JEU ===

def play(grid: State, player: Player, action: Action) -> State:
    """Met à jour la grille avec l'action du joueur."""
    if action not in legals(grid):
        return grid
    g = grid_tuple_to_grid_list(grid)
    g[action[0]][action[1]] = player
    return grid_list_to_grid_tuple(g)


def next_player(player: Player) -> Player:
    return O if player == X else X


# === STRATÉGIES DE JEU ===

def strategy_brain(grid: State, player: Player) -> Action:
    """Demande à l'utilisateur de saisir une action."""
    player_str = "X" if player == X else "O"
    print(f"\nÀ vous de jouer, placez un {player_str} sur une case (x,y) : ", end="")
    s = input()
    print()
    return ast.literal_eval(s)


def strategy_first_legal(grid: State, player: Player) -> Action:
    """Joue le premier coup légal trouvé."""
    return legals(grid)[0]


def strategy_random(grid: State, player: Player) -> Action:
    """Joue un coup aléatoire parmi les coups légaux."""
    actions = legals(grid)
    return random.choice(actions)


# === ALGORITHMES MINMAX ET ALPHA-BETA ===

def memoize(f: Callable) -> Callable:
    """Décorateur pour mémoïser une fonction."""
    cache = {}

    def g(*args):
        if args in cache:
            return cache[args]
        val = f(*args)
        cache[args] = val
        return val

    return g


@memoize
def minmax(grid: State, player: Player) -> Score:
    """Renvoie le meilleur score possible pour le joueur courant."""
    if final(grid):
        return score(grid)
    if player == X:
        return max(minmax(play(grid, X, action), O) for action in legals(grid))
    else:
        return min(minmax(play(grid, O, action), X) for action in legals(grid))


@memoize
def minmax_action(grid: State, player: Player, depth: int = 9) -> Tuple[Score, Action]:
    """Renvoie le score optimal et l'action qui y mène."""
    if depth == 0 or final(grid):
        return score(grid), (-1, -1)
    best_action = (-1, -1)
    if player == X:
        value = -math.inf
        for action in legals(grid):
            g = play(grid, X, action)
            v = minmax_action(g, O, depth - 1)[0]
            if v > value:
                best_action = action
                value = v
        return value, best_action
    else:
        value = math.inf
        for action in legals(grid):
            g = play(grid, O, action)
            v = minmax_action(g, X, depth - 1)[0]
            if v < value:
                best_action = action
                value = v
        return value, best_action


def strategy_minmax(grid: State, player: Player) -> Action:
    """Joue l'action optimale selon MinMax."""
    return minmax_action(grid, player)[1]


@memoize
def alphabeta_action(
        grid: State, player: Player, depth: int = 9, alpha: float = -math.inf, beta: float = math.inf
) -> Tuple[Score, Action]:
    """Renvoie le score optimal et l'action qui y mène (Alpha-Beta pruning)."""
    if depth == 0 or final(grid):
        return score(grid), (-1, -1)
    best_action = (-1, -1)
    if player == X:
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
    else:
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


def strategy_alphabeta(grid: State, player: Player) -> Action:
    """Joue l'action optimale selon Alpha-Beta pruning."""
    return alphabeta_action(grid, player)[1]


@memoize
def minmax_actions(grid: State, player: Player, depth: int = 9) -> Tuple[Score, List[Action]]:
    """Renvoie le score optimal et la liste des actions qui y mènent."""
    if final(grid) or depth == 0:
        return score(grid), []
    actions = legals(grid)
    best_score = -math.inf if player == X else math.inf
    best_actions = []
    for action in actions:
        g = play(grid, player, action)
        v, _ = minmax_actions(g, next_player(player), depth - 1)
        if (player == X and v > best_score) or (player == O and v < best_score):
            best_score = v
            best_actions = [action]
        elif v == best_score:
            best_actions.append(action)
    return best_score, best_actions


def strategy_minmax_random(grid: State, player: Player) -> Action:
    """Joue aléatoirement parmi les actions optimales (MinMax)."""
    _, actions = minmax_actions(grid, player)
    return random.choice(actions) if actions else (-1, -1)


@memoize
def alphabeta_actions(
        grid: State, player: Player, depth: int = 9, alpha: float = -math.inf, beta: float = math.inf
) -> Tuple[Score, List[Action]]:
    """Renvoie le score optimal et la liste des actions qui y mènent (Alpha-Beta)."""
    if final(grid) or depth == 0:
        return score(grid), []
    actions = legals(grid)
    best_score = -math.inf if player == X else math.inf
    best_actions = []
    for action in actions:
        g = play(grid, player, action)
        v, _ = alphabeta_actions(g, next_player(player), depth - 1, alpha, beta)
        if (player == X and v > best_score) or (player == O and v < best_score):
            best_score = v
            best_actions = [action]
        elif v == best_score:
            best_actions.append(action)
        if player == X:
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        else:
            beta = min(beta, best_score)
            if beta <= alpha:
                break
    return best_score, best_actions


def strategy_alphabeta_random(grid: State, player: Player) -> Action:
    """Joue aléatoirement parmi les actions optimales (Alpha-Beta)."""
    _, actions = alphabeta_actions(grid, player)
    return random.choice(actions) if actions else (-1, -1)


# === BOUCLE PRINCIPALE DE JEU ===

def tictactoe(strategy_X: Strategy, strategy_O: Strategy, debug: bool = False) -> Score:
    """Boucle principale du jeu jusqu'à la victoire ou match nul."""
    g = EMPTY_GRID
    if debug:
        pprint(g)
    current_player = X
    strategies = {X: strategy_X, O: strategy_O}
    while not final(g):
        action = strategies[current_player](g, current_player)
        g = play(g, current_player, action)
        if debug:
            pprint(g)
        if line(g, current_player):
            if debug:
                print(f"Fin du jeu ! Le joueur {'X' if current_player == X else 'O'} gagne.")
            return score(g)
        current_player = next_player(current_player)
    if debug:
        print("Match nul !")
    return score(g)


if __name__ == "__main__":
    # Partie entre deux IA (AlphaBeta vs Premier coup légal)
    tictactoe(strategy_alphabeta_random, strategy_first_legal, debug=True)
