import ast

Grid = tuple[tuple[int, ...], ...]
State = Grid
Action = tuple[int, int]
Player = int
Score = float

DRAW = 0
EMPTY = 0
X = 1
O = 2
TAILLE = 4

EMPTY_GRID: Grid = ((0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
GRID_0: Grid = ((0, 0, 0, 0), (0, O, X, 0), (0, X, O, 0), (0, 0, 0, 0))


def pprint(grid: Grid):
    """Affichage de la grille de jeu"""
    for row in grid:
        for cell in row:
            if cell in (EMPTY, 0):
                print(".", end=" ")
            elif cell in (X, 1):
                print("X", end=" ")
            elif cell in (O, 2):
                print("O", end=" ")
        print()
    print()


def grid_tuple_to_grid_list(grid: Grid) -> list[list[int]]:
    """Convertit une grille de tuples en une grille de listes"""
    return list(list(i) for i in grid)


def grid_list_to_grid_tuple(grid: list[list[int]]) -> Grid:
    """Convertit une grille de listes en une grille de tuples"""
    return tuple(tuple(i) for i in grid)


def horizontal(grid: State, player: Player, action: Action) -> list[Action]:
    """
    Tous les pions adversaires à gauche ou à droite de ce nouveau pion
    placé seront retournés, à condition que les pions adversaires soient pris
    "en sandwich" entre deux pions du joueur courant.
    """
    x, y = action
    if grid[x][y] != EMPTY:
        return []  # déjà un pion placé à cette position

    positions = []
    adversaire = X if player == O else O

    # parcourir à gauche
    positions_tmp: list[Action] = []
    for i in range(y - 1, -1, -1):  # reculer sur la ligne
        if grid[x][i] == adversaire:
            positions_tmp.append((x, i))
        elif grid[x][i] == player:  # on a atteint l'autre bout du "sandwich"
            positions.extend(positions_tmp)
            break
        else:
            break  # pas de pion du joueur courant en vue

    # parcourir à droite
    positions_tmp: list[Action] = []
    for i in range(y + 1, TAILLE):  # avancer sur la ligne
        if grid[x][i] == adversaire:
            positions_tmp.append((x, i))
        elif grid[x][i] == player:  # on a atteint l'autre bout du "sandwich"
            positions.extend(positions_tmp)
            break
        else:
            break  # pas de pion du joueur courant en vue

    return positions


def vertical(grid: State, player: Player, action: Action) -> list[Action]:
    """
    Tous les pions adversaires au-dessus ou en dessous de ce nouveau pion
    placé seront retournés, à condition que les pions adversaires soient pris
    "en sandwich" entre deux pions du joueur courant.
    """
    x, y = action
    if grid[x][y] != EMPTY:
        return []  # déjà un pion placé à cette position

    positions = []
    adversaire = X if player == O else O

    # parcourir à gauche
    positions_tmp: list[Action] = []
    for i in range(x - 1, -1, -1):
        if grid[i][y] == adversaire:
            positions_tmp.append((i, y))
        elif grid[i][y] == player:
            positions.extend(positions_tmp)
            break
        else:
            break

    # parcourir à droite
    positions_tmp: list[Action] = []
    for i in range(x + 1, TAILLE):
        if grid[i][y] == adversaire:
            positions_tmp.append((i, y))
        elif grid[i][y] == player:
            positions.extend(positions_tmp)
            break
        else:
            break

    return positions


def diagonal_1(grid: State, player: Player, action: Action) -> list[Action]:
    """
    Examine la diagonale anti-bissectrice (de haut-droite vers bas-gauche).
    Retourne la liste des positions à retourner suite à l'action.
    """
    x, y = action
    if grid[x][y] != EMPTY:
        return []
    adversaire = O if player == X else X
    positions = []

    # Directions : (-1, -1) (haut-gauche), (+1, +1) (bas-droit)
    for dx, dy in [(-1, -1), (1, 1)]:
        tmp = []
        i, j = x + dx, y + dy
        while 0 <= i < TAILLE and 0 <= j < TAILLE:
            if grid[i][j] == adversaire:
                tmp.append((i, j))
            elif grid[i][j] == player:
                if tmp:
                    positions.extend(tmp)
                break
            else:
                break
            i += dx
            j += dy

    return positions


def diagonal_2(grid: State, player: Player, action: Action) -> list[Action]:
    """
    Examine la diagonale bissectrice (de bas-gauche vers haut-droit).
    Retourne la liste des positions à retourner suite à l'action.
    """
    x, y = action
    if grid[x][y] != EMPTY:
        return []
    adversaire = O if player == X else X
    positions = []

    # Directions : (-1, -1) (haut-gauche), (+1, +1) (bas-droit)
    for dx, dy in [(-1, 1), (1, -1)]:
        tmp = []
        i, j = x + dx, y + dy
        while 0 <= i < TAILLE and 0 <= j < TAILLE:
            if grid[i][j] == adversaire:
                tmp.append((i, j))
            elif grid[i][j] == player:
                if tmp:
                    positions.extend(tmp)
                break
            else:
                break
            i += dx
            j += dy

    return positions


def legals(grid: State, player: Player) -> list[Action]:
    """Retourne la liste des positions avec lesquelles le joueur peut jouer un coup légal."""
    all_positions = [(i, j) for i in range(TAILLE) for j in range(TAILLE)]
    actions_possibles: list[Action] = []
    for pos in all_positions:
        # On concatène toutes les directions
        retournables = (
                horizontal(grid, player, pos) +
                vertical(grid, player, pos) +
                diagonal_1(grid, player, pos) +
                diagonal_2(grid, player, pos)
        )
        if retournables:
            actions_possibles.append(pos)
    return actions_possibles


def final(grid: State) -> bool:
    """Retourne True si la partie est terminée (aucun joueur ne peut jouer), sinon False."""
    return len(legals(grid, X)) == 0 and len(legals(grid, O)) == 0


def play(grid: State, player: Player, action: Action) -> State:
    """Met à jour la grille avec l'action du joueur et retourne les pions adverses."""
    if action not in legals(grid, player):
        return grid

    g = grid_tuple_to_grid_list(grid)
    x, y = action
    g[x][y] = player

    a_retourner = (
            horizontal(grid, player, action) +
            vertical(grid, player, action) +
            diagonal_1(grid, player, action) +
            diagonal_2(grid, player, action)
    )

    # Retourner les pions
    for i, j in a_retourner:
        g[i][j] = player

    return grid_list_to_grid_tuple(g)


def nb_pion(grid: State, player: Player) -> float:
    """Compte le nombre de pions du joueur donné sur la grille."""
    return sum(cell == player for row in grid for cell in row)


def score(grid: State) -> Score:
    """
    Si c'est X qui forme une ligne, alors on affiche 1.
    Sinon si c'est O, on affiche -1.
    """
    score_x = nb_pion(grid, X)
    score_o = nb_pion(grid, O)

    if score_x > score_o:
        return 1
    if score_x < score_o:
        return -1
    return 0


def main():
    print("[JEU OTHELLO-REVERSI]")
    g = GRID_0
    player = O

    while not final(g):
        player = X if player == O else O
        print(f"\nAu joueur {'X' if player == X else 'O'} de jouer :")
        pprint(g)
        action_str = input("Entre une case où tu veux poser ton pion (x,y): ")

        action = ast.literal_eval(action_str)
        if not (isinstance(action, tuple) and len(action) == 2):
            raise ValueError

        if action not in legals(g, player):
            print("Coup illégal, choisis une autre case.")
            continue

        g = play(g, player, action)

    print("Plateau final :")
    pprint(g)
    s = score(g)
    if s == 1:
        print("Le gagnant est X")
    elif s == -1:
        print("Le gagnant est O")
    else:
        print("Égalité !")


if __name__ == "__main__":
    main()
