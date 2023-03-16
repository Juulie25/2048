#Définition des variables
# s -> configuration actuelle du plateau (temps t)
# s == grid

# s0 -> configuration du plateau a t+1, lorsque l'action de déplacement a été faite = AFTER STATE
# s00 -> configuration du plateau a t+2, une nouvelle tuile est ajoutée
# r -> reward : 
# a -> action réalisée (G/D/H/B)
# P(x) -> fonction de transition 
# R(x) -> fonction de reward
import pygame

def __init__(self):
    # grille complète
    self.grid = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]

    self.tilesColor = {
        0: "#BFB3A5",
        2: "#FAE7E0",
        4: "#FAE5CA",
        8: "#FBB17A",
        16: "#DF9F74",
        32: "#E08A72",
        64: "#FD5B42",
        128: "#FAD177",
        256: "#F7D067",
        512: "#F9CA58",
        1024: "#F9CA58",
        2048: "#FBC52D",
        4096: "#F66574",
        8192: "#F34B5C",
        16384: "#EB4039",
        32768: "#70B3D8",
        65536: "#5EA1E4",
        131072: "#007FC2"
    }

    self.actions = {
        "UP",
        "DOWN",
        "LEFT",
        "RIGHT"
    }

    self.score = 0
    self.nbMove = 0
    self.add_new_tile()
    self.add_new_tile()

    pygame.init()
    self.font = pygame.font.SysFont("Arial", 36)
    self.screen = pygame.display.set_mode((400, 500))
    pygame.display.set_caption("2048 Game")

    while not is_game_over():
        action = evaluate()
        self.score += make_move(self.grid,action)
    #learn pour améliorer ses coups 


#Copie proprement les grilles
def gridCopy(grid):
    res = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(0,4):
        for j in range(0,4):
            res[i][j] = grid[i][j]
    return res

def is_game_over(self):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
    if empty_cells: return False
    for i in range(3):
        for j in range(3):
            if self.grid[i][j] == self.grid[i + 1][j] or self.grid[i][j] == self.grid[i][j + 1]:
                return False
    # Comparer les dernières lignes et colonnes séparément
    for i in range(3):
        if self.grid[3][i] == self.grid[3][i + 1]:
            return False
        if self.grid[i][3] == self.grid[i + 1][3]:
            return False
    return True


def evaluate(self):
    action_choisie = None
    score = 0
    espace = 0
    list_grid = [0 for _ in range(4)]

    #On définit les 4 copies de la grille actuelle pour appliquer sur chacune d'entre elle une action
    for i in range(len(list_grid)):
        list_grid[i] = gridCopy(self.grid)
        if i == 0:
            score_tmp = move_tiles_right(list_grid[i])
            if score_tmp > score:
                score = score_tmp
                action_choisie = "right"
            else:
                if score == score_tmp:
                    espace_tmp = espace_libere(list_grid[i])
                    if espace_tmp > espace:
                        espace = espace_tmp
                        action_choisie = "right"
        if i == 1:
            score_tmp = move_tiles_left(list_grid[i])
            if score_tmp > score:
                score = score_tmp
                action_choisie = "left"
            else:
                if score == score_tmp:
                    espace_tmp = espace_libere(list_grid[i])
                    if espace_tmp > espace:
                        espace = espace_tmp
                        action_choisie = "left"
        if i == 2:
            score_tmp = move_tiles_up(list_grid[i])
            if score_tmp > score:
                score = score_tmp
                action_choisie = "up"
            else:
                if score == score_tmp:
                    espace_tmp = espace_libere(list_grid[i])
                    if espace_tmp > espace:
                        espace = espace_tmp
                        action_choisie = "up"
        if i == 3:
            score_tmp = move_tiles_down(list_grid[i])
            if score_tmp > score:
                score = score_tmp
                action_choisie = "down"
            else:
                if score == score_tmp:
                    espace_tmp = espace_libere(list_grid[i])
                    if espace_tmp > espace:
                        espace = espace_tmp
                        action_choisie = "left"
    return action_choisie

def move_tiles_left(grid):
    score = 0
    for row in grid:
        row.sort(key=lambda x: 0 if x == 0 else 1, reverse=True)
        for i in range(3):
            if row[i] == row[i + 1]:
                row[i] *= 2
                score += row[i]
                row[i + 1] = 0
        row.sort(key=lambda x: 0 if x == 0 else 1, reverse=True)
    return score


def move_tiles_right(grid):
    score = 0
    for row in grid:
        row.sort(key=lambda x: 0 if x == 0 else 1)
        for i in range(3, 0, -1):
            if row[i] == row[i - 1]:
                row[i] *= 2
                score += row[i]
                row[i - 1] = 0
        row.sort(key=lambda x: 0 if x == 0 else 1)
    return score


def move_tiles_up(grid):
    score = 0
    for j in range(4):
        col = [grid[i][j] for i in range(4)]
        col.sort(key=lambda x: 0 if x == 0 else 1, reverse=True)
        for i in range(3):
            if col[i] == col[i + 1]:
                col[i] *= 2
                score += col[i]
                col[i + 1] = 0
        col.sort(key=lambda x: 0 if x == 0 else 1, reverse=True)
        for i in range(4):
            grid[i][j] = col[i]
    return score

def move_tiles_down(grid):
    score = 0
    for j in range(4):
        col = [grid[i][j] for i in range(4)]
        col.sort(key=lambda x: 0 if x == 0 else 1)
        for i in range(3, 0, -1):
            if col[i] == col[i - 1]:
                col[i] *= 2
                score += col[i]
                col[i - 1] = 0
        col.sort(key=lambda x: 0 if x == 0 else 1)
        for i in range(4):
            grid[i][j] = col[i]
    return score

def espace_libere(grid):
    espace_libre = 0
    for x in len(grid):
        for y in len(grid[0]):
            if grid[x,y] == 0:
                espace_libre+1
    return espace_libre


def playGame() :
    score = 0
    s = INITIALIZE GAME STATE
    while (not IS TERMINAL STATE(s)):
        a =  arg maxa0∈A(s) EVALUATE(s, a)
        r, s0, s00 = MAKE MOVE(s, a)
    if LEARNING ENABLED :
        LEARN EVALUATION(s, a, r, s0, s00)
    score = score + r
    s = s00
    return score

# for a given state s ∈ S and action a ∈ A(s) returns a received reward and an observed state transition
def makeMove(s,a):
    s0, r = COMPUTE AFTERSTATE(s, a)
    s00 = ADD RANDOM TILE(s0)
    return (r, s0, s00)

#Les couples de méthodes ne se basent pas sur les memes configurations de départ 

#EVALUATE 
# attempts to measure the utility of taking each possible action a ∈ A(s) in the current state s
# moves are selected to maximize the value returned by this function
#renvoie la meilleure action possible


# LEARN EVALUATE 
# adjusts the evaluation function on the basis of the observed experience represented by a tuple (s, a, r, s0, s00)


#The action evaluation function and Q-LEARNING ->  Evaluating actions
def evaluate(s,a):
    return Va(s)

def learnEvaluation(s, a, r, s0, s00):
    vnext = maxa0∈A(s00) Va0 (s00)
    Va(s) = Va(s) + α(r + vnext − Va(s))


#==============================AUTRES IDEES POUR LA SUITE==============================#

# #The state evaluation function and TD(0) ->  Evaluating states
# #évaluer les états dans lesquels ils aboutissent avec la fonction de valeur d'état V (s)
# #méthode plus lente car doit évaluer tous les coups possibles à chaque fois
# def evaluate(s,a):
#     s0, r = COMPUTE AFTERSTATE(s, a)
#     S00 = ALL POSSIBLE NEXT STATES(s0)
#     return r + (somme s00∈S00) P(s, a, s00)V (s00)
#
# def learnEvaluation(s, a, r, s0, s00):
#     V (s) = V (s) + αlpha(r + V (s00) − V (s))
#
# #The afterstate evaluation function ->  Evaluating afterstates
# # evaluate moves can be regarded as a combination of the action evaluation and the state evaluation
# # updates the value of the recently observed afterstate
# def evaluate(s,a):
#     s0, r = COMPUTE AFTERSTATE(s, a)
#     return r + V(s0)
#
# def learnEvaluation(s, a, r, s0, s00):
#     #determining the next action that would be taken
#     anext = arg maxa0∈A(s00) EVALUATE(s00, a0)
#     #compute the next reward and the new afterstate
#     s0next, rnext = COMPUTE AFTERSTATE(s00, anext)
#     V (s0) = V (s0) + α(rnext + V (s0next) − V (s0))
#
# # n-tuple network
# # For a given board state s, it calculates the sum of values returned by the individual n-tuples