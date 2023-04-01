import pickle
import math
import random
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"  # Ca permet d'éviter le msg de bienvenue
import pygame


class game2048:
    def __init__(self):

        # Grille complète
        self.grid = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        # Choix des couleurs
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

        # Initialisation des différents paramètres du jeux
        self.score = 0
        self.nbMove = 0
        self.add_new_tile()
        self.add_new_tile()

        # Active l'apprentissage
        self.learn = True

        # Initialisation des différents tableaux et dicos contenant les poids
        tuples = [0] * 17
        for i in range(17):
            tuples[i] = {"0000": 0}

        self.tuples = tuples

        # Initialisation du jeux avec pygame
        pygame.init()
        self.font = pygame.font.SysFont("Arial", 36)
        self.screen = pygame.display.set_mode((400, 500))
        pygame.display.set_caption("2048 Game")

    # Ajout de nouvelles tuiles
    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    # Vérifie si la game est fini
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

    # Copie proprement la grille
    def grid_copy(self):
        res = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(0, 4):
            for j in range(0, 4):
                res[i][j] = self.grid[i][j]
        return res

    # Définit la meilleure tuile de la grille
    def best_tile(self):
        max_tile = self.grid[0][0]
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] > max_tile: max_tile = self.grid[i][j]
        return max_tile

    # Choisit la meilleure actions a faire
    # SUREMENT POSSIBLE A OPTIMISER
    # IL FAUDRAIT TROUVER UN MOYEN DE REGARDER LORSQUE UN MOVE NE CHANGE RIEN => CA EVITERAI QUE LE PROG BOUCLE ET QUE LA GRILLE BLOQUE...
    def best_choice(self):
        testL = self.grid_copy()
        self.move_tiles_left(testL)
        valeurL = self.evaluate(testL)
        testR = self.grid_copy()
        self.move_tiles_right(testR)
        valeurR = self.evaluate(testR)
        testU = self.grid_copy()
        self.move_tiles_up(testU)
        valeurU = self.evaluate(testU)
        testD = self.grid_copy()
        self.move_tiles_down(testD)
        valeurD = self.evaluate(testD)

        # Fait un choix aléatoire tout les 10% du temps
        if random.random() >= 0.90:
            choix = random.choice([valeurL, valeurR, valeurU, valeurD])

            if choix == valeurL:
                self.grid = testL
                self.reward = self.scoreL
            if choix == valeurR:
                self.grid = testR
                self.reward = self.scoreR
            if choix == valeurU:
                self.grid = testU
                self.reward = self.scoreU
            if choix == valeurD:
                self.grid = testD
                self.reward = self.scoreD
        else:
            # DOIT CHANGER MAX, IL NE SAIT PAS TRANCHER EN CAS D'EGALITE
            choix = max(valeurL, valeurR, valeurU, valeurD)

            if choix == valeurL:
                self.grid = testL
                self.reward = self.scoreL
            if choix == valeurR:
                self.grid = testR
                self.reward = self.scoreR
            if choix == valeurU:
                self.grid = testU
                self.reward = self.scoreU
            if choix == valeurD:
                self.grid = testD
                self.reward = self.scoreD

    # Renvoi une valeur pour évaluer une grille en fonction des poids
    def evaluate(self, grid):
        res = 0
        for i in range(17):
            if self.read_tuple(grid, i) in self.tuples[i]:
                res += self.tuples[i][self.read_tuple(grid, i)]
        return res

    # Apprend tout au long de la partie en modifiant les poids
    def learn_evaluation(self):
        rew = math.log2(self.reward) if self.reward > 0 else 0
        alpha = 0.0050  # D'après l'étude du document...

        for i in range(17):
            if self.read_tuple(self.initial, i) in self.tuples[i]:
                if self.read_tuple(self.grid, i) in self.tuples[i]:
                    res_next = self.tuples[i][self.read_tuple(self.grid, i)]
                else:
                    res_next = 0
                self.tuples[i][self.read_tuple(self.initial, i)] = self.tuples[i][
                                                                       self.read_tuple(self.initial, i)] + alpha * (
                                                                           rew + res_next - self.tuples[i][
                                                                       self.read_tuple(self.initial, i)])
            else:
                self.tuples[i][self.read_tuple(self.initial, i)] = 0

    # Bouge les tuiles "bougeable" sur la gauche et renvoi un score
    def move_tiles_left(self, grid):
        self.scoreL = 0
        for row in grid:
            row.sort(key=lambda x: 0 if x == 0 else 1, reverse=True)
            for i in range(3):
                if row[i] == row[i + 1]:
                    row[i] *= 2
                    self.scoreL += row[i]
                    row[i + 1] = 0
            row.sort(key=lambda x: 0 if x == 0 else 1, reverse=True)
        return grid

    # Bouge les tuiles "bougeable" sur la droite et renvoi un score
    def move_tiles_right(self, grid):
        self.scoreR = 0
        for row in grid:
            row.sort(key=lambda x: 0 if x == 0 else 1)
            for i in range(3, 0, -1):
                if row[i] == row[i - 1]:
                    row[i] *= 2
                    self.scoreR += row[i]
                    row[i - 1] = 0
            row.sort(key=lambda x: 0 if x == 0 else 1)
        return grid

    # Bouge les tuiles "bougeable" vers le haut et renvoi un score
    def move_tiles_up(self, grid):
        self.scoreU = 0
        for j in range(4):
            col = [grid[i][j] for i in range(4)]
            col.sort(key=lambda x: 0 if x == 0 else 1, reverse=True)
            for i in range(3):
                if col[i] == col[i + 1]:
                    col[i] *= 2
                    self.scoreU += col[i]
                    col[i + 1] = 0
            col.sort(key=lambda x: 0 if x == 0 else 1, reverse=True)
            for i in range(4):
                grid[i][j] = col[i]
        return grid

    # Bouge les tuiles "bougeable" vers le bas et renvoi un score
    def move_tiles_down(self, grid):
        self.scoreD = 0
        for j in range(4):
            col = [grid[i][j] for i in range(4)]
            col.sort(key=lambda x: 0 if x == 0 else 1)
            for i in range(3, 0, -1):
                if col[i] == col[i - 1]:
                    col[i] *= 2
                    self.scoreD += col[i]
                    col[i - 1] = 0
            col.sort(key=lambda x: 0 if x == 0 else 1)
            for i in range(4):
                grid[i][j] = col[i]
        return grid

    # Renvoie le poid inscrit dans les tableaux du tuple choisi
    def read_tuple(self, grille, i):
        if i < 4:
            res0 = math.log2(grille[i][0]) if grille[i][0] > 0 else 0
            res1 = math.log2(grille[i][1]) if grille[i][1] > 0 else 0
            res2 = math.log2(grille[i][2]) if grille[i][2] > 0 else 0
            res3 = math.log2(grille[i][3]) if grille[i][3] > 0 else 0
            return str(int(res0)) + str(int(res1)) + str(int(res2)) + str(int(res3))
        if 4 <= i < 8:
            res0 = math.log2(grille[0][i % 4]) if grille[0][i % 4] > 0 else 0
            res1 = math.log2(grille[1][i % 4]) if grille[1][i % 4] > 0 else 0
            res2 = math.log2(grille[2][i % 4]) if grille[2][i % 4] > 0 else 0
            res3 = math.log2(grille[3][i % 4]) if grille[3][i % 4] > 0 else 0
            return str(int(res0)) + str(int(res1)) + str(int(res2)) + str(int(res3))
        if i >= 8:
            if 7 < i < 11: a = 0
            if 11 <= i < 14: a = 1
            if i >= 14: a = 2
            res0 = math.log2(grille[a][a]) if grille[a][a] > 0 else 0
            res1 = math.log2(grille[a][a + 1]) if grille[a][a + 1] > 0 else 0
            res2 = math.log2(grille[a + 1][a]) if grille[a + 1][a] > 0 else 0
            res3 = math.log2(grille[a + 1][a + 1]) if grille[a + 1][a + 1] > 0 else 0
            return str(int(res0)) + str(int(res1)) + str(int(res2)) + str(int(res3))

    # Dessine la fenêtre de jeu
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

    # Gère le déroulement du jeu
    def run(self):
        if os.path.isfile('tuples2048'):
            with open('tuples2048', 'rb') as file:
                print("Lecture du fichier des tuples")
                self.tuples = pickle.load(file)
        else:
            print("Erreur : Le fichier n'existe pas")
        self.draw()

        while not self.is_game_over():
            self.initial = self.grid_copy()
            self.reward = 0
            self.best_choice()
            self.score += self.reward
            if self.grid != self.initial:
                self.nbMove = self.nbMove + 1
                self.add_new_tile()
                self.draw()
            if self.learn:
                self.learn_evaluation()
            pygame.time.wait(50)

        print("---------------")
        print("GAME OVER")
        print("Score : ", self.score)
        print("NbMove ", self.nbMove)
        print("Best tile :", self.best_tile())
        print("---------------\n")

        with open('tuples2048', 'wb') as file:
            print("Mise à jour du fichier des tuples")
            pickle.dump(self.tuples, file)
        pygame.quit()
        quit()


# On définit quelle classe est un jeu et on le lance avec pygame
game = game2048()
game.run()

# ==============================AUTRES IDEES POUR LA SUITE==============================#

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
