#Définition des variables
# s -> configuration actuelle du plateau (temps t)
# s == grid

# s0 -> configuration du plateau a t+1, lorsque l'action de déplacement a été faite = AFTER STATE
# s00 -> configuration du plateau a t+2, une nouvelle tuile est ajoutée
# r -> reward : score
# a -> action réalisée (G/D/H/B)
# P(x) -> fonction de transition 
# R(x) -> fonction de reward

# map avec état action en clé et la valeur en valeur
# fichier à enregister sur une représentation binaire (serialisation) et à lire a chaque nouvelle partie

import pygame
import pickle
import math
import random

from collections import defaultdict


class game2048():
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
            "LEFT",
            "RIGHT",
            "UP",
            "DOWN"
        }

        self.afterstate = self.grid
        self.addtile = self.grid
        self.score = 0
        self.nbMove = 0
        self.add_new_tile()
        self.add_new_tile()
        # self.learn = True

        tuple_l = []
        tuple_r = []
        tuple_u = []
        tuple_d = []
        for i in range (17):
            # il aime pas ca...
            tuple_l[i] = {"0000":0}
            tuple_r[i] = {"0000":0}
            tuple_u[i] = {"0000":0}
            tuple_d[i] = {"0000":0}
            # tuple_l[i] = defaultdict(lambda : 0)
            # tuple_d[i] = {}

        self.v_actions = [tuple_l, tuple_r, tuple_u, tuple_d]

        pygame.init()
        self.font = pygame.font.SysFont("Arial", 36)
        self.screen = pygame.display.set_mode((400, 500))
        pygame.display.set_caption("2048 Game")

        with open('tuples2048', 'wb') as file:
            print("creation fichier")
            pickle.dump(self.v_actions, file)

        while not self.is_game_over():
            #doit évaluer les 4 moves pour prendre le meilleur dans action
            moveL = self.evaluate("LEFT")
            moveR = self.evaluate("RIGHT")
            moveU = self.evaluate("UP")
            moveD = self.evaluate("DOWN")
            if (max(moveL,moveR,moveU,moveD) == moveL): act = "LEFT"
            if (max(moveL,moveR,moveU,moveD) == moveR): act = "RIGHT"
            if (max(moveL,moveR,moveU,moveD) == moveU): act = "UP"
            if (max(moveL,moveR,moveU,moveD) == moveD): act = "DOWN"
            self.score += self.make_move(self.grid, act)
            self.afterstate = self.grid
            self.nbMove = self.nbMove + 1
            self.add_new_tile()
            self.addtile = self.grid
        # if self.learn:
        #     learn_evaluation(self, action, reward)

    #Ajoute des nouvelles tuiles
    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    # Copie proprement les grilles
    def grid_copy(grid):
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

    def evaluate(self, action):
        reward = 0
        if(action == "LEFT"): act = 1
        if(action == "RIGHT"): act = 2
        if(action == "UP"): act = 3
        if(action == "DOWN"): act = 4
        a = self.v_actions[act]
        for i in range(17):
            if self.read_tuple(i) in a:
                reward += a[i][self.read_tuple(i)]
        return reward

    # grid, action, reward, grid_afterstate, grid_addtile
    # def learn_evaluation(self, action, reward):
        # i = 1
        # a partir de S'' on regarde les 4 actions et on prend la meilleure valeur => dans les tables,
        # calculer les coordonnées pour tous les n-tuples et faire la somme des 3 tuples et on la renvoie
        # puis récupérer le max entre les 4 valeurs
        # vnext = maxa0∈A(s00) Va0 (s00)
        # vnext = "oui"
        # Va(s) = Va(s) + α(r + vnext − Va(s))
        # self.v_actions[action] = self.v_actions[action] + alpha*(reward + vnext-self.v_actions[action])

    def move_tiles_left(self):
        score = 0
        for row in self:
            row.sort(key=lambda x: 0 if x == 0 else 1, reverse=True)
            for i in range(3):
                if row[i] == row[i + 1]:
                    row[i] *= 2
                    score += row[i]
                    row[i + 1] = 0
            row.sort(key=lambda x: 0 if x == 0 else 1, reverse=True)
        return score

    def move_tiles_right(self):
        score = 0
        for row in self:
            row.sort(key=lambda x: 0 if x == 0 else 1)
            for i in range(3, 0, -1):
                if row[i] == row[i - 1]:
                    row[i] *= 2
                    score += row[i]
                    row[i - 1] = 0
            row.sort(key=lambda x: 0 if x == 0 else 1)
        return score

    def move_tiles_up(self):
        score = 0
        for j in range(4):
            col = [self[i][j] for i in range(4)]
            col.sort(key=lambda x: 0 if x == 0 else 1, reverse=True)
            for i in range(3):
                if col[i] == col[i + 1]:
                    col[i] *= 2
                    score += col[i]
                    col[i + 1] = 0
            col.sort(key=lambda x: 0 if x == 0 else 1, reverse=True)
            for i in range(4):
                self[i][j] = col[i]
        return score

    def move_tiles_down(self):
        score = 0
        for j in range(4):
            col = [self[i][j] for i in range(4)]
            col.sort(key=lambda x: 0 if x == 0 else 1)
            for i in range(3, 0, -1):
                if col[i] == col[i - 1]:
                    col[i] *= 2
                    score += col[i]
                    col[i - 1] = 0
            col.sort(key=lambda x: 0 if x == 0 else 1)
            for i in range(4):
                self[i][j] = col[i]
        return score

    def espace_libere(grid):
        espace_libre = 0
        for x in len(grid):
            for y in len(grid[0]):
                if grid[x,y] == 0:
                    espace_libre = espace_libre+1
        return espace_libre

    def make_move(grid, action):
        if action == "LEFT":
            return grid.move_tiles_left()
        if action == "RIGHT":
            return grid.move_tiles_right()
        if action == "UP":
            return grid.move_tiles_up()
        if action == "DOWN":
            return grid.move_tiles_down()

    # renvoie la valeur de la ligne
    def read_tuple(self,i):
        if i < 4:
            res0 = math.log2(self.grid[i][0])
            res1 = math.log2(self.grid[i][1])
            res2 = math.log2(self.grid[i][2])
            res3 = math.log2(self.grid[i][3])
            return str(int(res0)) + str(int(res1)) + str(int(res2)) + str(int(res3))
        if 4 <= i < 8:
            res0 = math.log2(self.grid[0][i])
            res1 = math.log2(self.grid[1][i])
            res2 = math.log2(self.grid[2][i])
            res3 = math.log2(self.grid[3][i])
            return str(int(res0)) + str(int(res1)) + str(int(res2)) + str(int(res3))
        if i>=8 :
            if i>7 & i<11:a=0
            if i>=11 & i<14:a=1
            if i>=14:a=2
            res0 = math.log2(self.grid[a][a])
            res1 = math.log2(self.grid[a][a+1])
            res2 = math.log2(self.grid[a+1][a])
            res3 = math.log2(self.grid[a+1][a+1])
            return str(int(res0)) + str(int(res1)) + str(int(res2)) + str(int(res3))

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.font = pygame.font.SysFont("Arial", 30)
        score_text = self.font.render("Score: " + str(self.score), True, (0, 0, 0))
        move_text = self.font.render("Move: " + str(self.nbMove), True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(move_text, (10, 45))
        pygame.draw.rect(self.screen, "#AD9C90", (0, 100, 400, 400))
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(self.screen, self.tilesColor[self.grid[i][j]], (j * 100 + 10, i * 100 + 110, 80, 80))
                if self.grid[i][j] != 0:
                    size = 0 if len(str(self.grid[i][j])) - 4 < 0 else len(str(self.grid[i][j])) - 3
                    self.font = pygame.font.SysFont("Arial", 32 - 4 * size)
                    text = self.font.render(str(self.grid[i][j]), True, (0, 0, 0))
                    text_rect = text.get_rect()
                    text_rect.center = (j * 100 + 50, i * 100 + 150)
                    self.screen.blit(text, text_rect)
        pygame.display.update()

    def run(self):
        self.draw()


game = game2048()
game.run()
#==============================PSEUDO CODE ==============================#
# def playGame() :
#     score = 0
#     s = INITIALIZE GAME STATE
#     while (not IS TERMINAL STATE(s)):
#         a =  arg maxa0∈A(s) EVALUATE(s, a)
#         r, s0, s00 = MAKE MOVE(s, a)
#     if LEARNING ENABLED :
#         LEARN EVALUATION(s, a, r, s0, s00)
#     score = score + r
#     s = s00
#     return score

# for a given state s ∈ S and action a ∈ A(s) returns a received reward and an observed state transition
# def makeMove(s,a):
#     s0, r = COMPUTE AFTERSTATE(s, a)
#     s00 = ADD RANDOM TILE(s0)
#     return (r, s0, s00)

#Les couples de méthodes ne se basent pas sur les memes configurations de départ 

#EVALUATE 
# attempts to measure the utility of taking each possible action a ∈ A(s) in the current state s
# moves are selected to maximize the value returned by this function
#renvoie la meilleure action possible


# LEARN EVALUATE 
# adjusts the evaluation function on the basis of the observed experience represented by a tuple (s, a, r, s0, s00)


#The action evaluation function and Q-LEARNING ->  Evaluating actions
# def evaluate(s,a):
#     return Va(s)
#
# def learnEvaluation(s, a, r, s0, s00):
#     vnext = maxa0∈A(s00) Va0 (s00)
#     Va(s) = Va(s) + α(r + vnext − Va(s))

#une table par état et par action
#Va(s) : somme des poids des n-tuples en fonction de l'action
# 4 fois la meme structure avec chaque structure qui contient n tables pour chaque tuples


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