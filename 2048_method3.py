import os
import math
import pickle
import random

# Suppression du message de bienvenu (faut import pygame après)
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


class game2048:
    def __init__(self):

        # Grille initiale
        self.grid = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        # Liste des couleurs
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
        self.moveNb = 0
        self.add_new_tile()
        self.add_new_tile()

        # Active l'apprentissage
        self.learn = True

        # Initialisation des différents tableaux et dictionnaires contenant les poids
        tuples = [0] * 17
        for i in range(17):
            tuples[i] = {"0000": 0}

        self.tuples = tuples

        # Initialisation du jeu avec pygame
        pygame.init()
        self.font = pygame.font.SysFont("Arial", 36)
        self.screen = pygame.display.set_mode((400, 500))
        pygame.display.set_caption("2048 Game")

    def add_new_tile(self):
        """
        Ajout d'une nouvelle tuile sur la grille
        """
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    # Vérifie si la game est fini
    def is_game_over(self):
        """
        Vérifie si auncun mouvement ne peut être effectué et donc si la partie est finie
        :return: True si la partie est finie, False sinon
        """
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

    def grid_copy(self):
        """
        Effectue une copie profonde de la grille de jeu actuelle
        :return: la copie de la grille
        """
        res = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(0, 4):
            for j in range(0, 4):
                res[i][j] = self.grid[i][j]
        return res

    def best_tile(self):
        """
        Récupère la tuile avec le score le plus élevé sur la grille
        :return: la tuile avec le meilleur score
        """
        max_tile = self.grid[0][0]
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] > max_tile: max_tile = self.grid[i][j]
        return max_tile

    def best_choice(self):
        """
        Définit la meilleure action a faire en fonction de la configuation de la grille
        """
        # On créer 4 grilles pour observer le résultat des 4 actions
        test1_l = self.grid_copy()
        self.move_tiles_left(test1_l)
        value_l = self.evaluate(test1_l, "LEFT") if test1_l != self.grid else 0

        test1_r = self.grid_copy()
        self.move_tiles_right(test1_r)
        value_r = self.evaluate(test1_r, "RIGHT") if test1_r != self.grid else 0

        test1_u = self.grid_copy()
        self.move_tiles_up(test1_u)
        value_u = self.evaluate(test1_u, "UP") if test1_u != self.grid else 0

        test1_d = self.grid_copy()
        self.move_tiles_down(test1_d)
        value_d = self.evaluate(test1_d, "DOWN") if test1_d != self.grid else 0

        # On tri une liste pour trouver la plus grande valeur
        # L'avantage de cette méthode est qu'elle fonctionne même en cas d'égalité
        list = [value_l, value_r, value_u, value_d]
        list.sort()

        # Permet d'afficher la liste des valeurs pour le choix
        # print(list)

        # On prend la meilleure action 90% du temps et le reste du temps on prend une action aléatoire
        choice = random.choice([value_l, value_r, value_u, value_d]) if random.random() >= 0.90 else list[-1]

        if choice == value_l:
            self.grid = test1_l
            self.reward = self.scoreL
        if choice == value_r:
            self.grid = test1_r
            self.reward = self.scoreR
        if choice == value_u:
            self.grid = test1_u
            self.reward = self.scoreU
        if choice == value_d:
            self.grid = test1_d
            self.reward = self.scoreD

    def evaluate(self, grid, action):
        """
        Evaluation de la grille en lui affectant une valeur en fonction de la disposition des tuiles
        :param grid: la grille à évaluer
        :return: le poids associé à la grille
        """
        value = 0
        if action == "UP":
            reward = self.move_tiles_up(grid)
            for i in range(17):
                if self.read_tuple(grid, i) in self.tuples[i]:
                    value += self.tuples[i][self.read_tuple(grid, i)]
        elif action == "DOWN":
            reward = self.move_tiles_down(grid)
            for i in range(17):
                if self.read_tuple(grid, i) in self.tuples[i]:
                    value += self.tuples[i][self.read_tuple(grid, i)]
        elif action == "RIGHT":
            reward = self.move_tiles_right(grid)
            for i in range(17):
                if self.read_tuple(grid, i) in self.tuples[i]:
                    value += self.tuples[i][self.read_tuple(grid, i)]
        else:
            reward = self.move_tiles_left(grid)
            for i in range(17):
                if self.read_tuple(grid, i) in self.tuples[i]:
                    value += self.tuples[i][self.read_tuple(grid, i)]
        return reward + value

    def learn_evaluation(self):
        # D'après l'étude du document
        alpha = 0.0050

        next_value = 0

        # On créer 4 grilles pour observer le résultat des 4 actions
        test2_l = self.grid_copy()
        reward_l = self.move_tiles_left(test2_l)
        value_l = self.evaluate(test2_l, "LEFT") if test2_l != self.grid else 0

        test2_r = self.grid_copy()
        reward_r = self.move_tiles_right(test2_r)
        value_r = self.evaluate(test2_r, "RIGHT") if test2_r != self.grid else 0

        test2_u = self.grid_copy()
        reward_u = self.move_tiles_up(test2_u)
        value_u = self.evaluate(test2_u, "UP") if test2_u != self.grid else 0

        test2_d = self.grid_copy()
        reward_d = self.move_tiles_down(test2_d)
        value_d = self.evaluate(test2_d, "DOWN") if test2_d != self.grid else 0

        # On tri une liste pour trouver la plus grande valeur
        # L'avantage de cette méthode est qu'elle fonctionne même en cas d'égalité
        list = [value_l, value_r, value_u, value_d]
        list.sort()

        choice = list[-1]

        if choice == value_l:
            next_grid = test2_l
            next_reward = reward_l
        if choice == value_r:
            next_grid = test2_r
            next_reward = reward_r
        if choice == value_u:
            next_grid = test2_u
            next_reward = reward_u
        if choice == value_d:
            next_grid = test2_d
            next_reward = reward_d

        for i in range(17):
            if self.read_tuple(self.intermediate, i) in self.tuples[i]:
                if self.read_tuple(next_grid, i) in self.tuples[i]:
                    next_value = self.tuples[i][self.read_tuple(next_grid, i)]
                else:
                    next_value = 0
                self.tuples[i][self.read_tuple(self.intermediate, i)] = \
                    self.tuples[i][self.read_tuple(self.intermediate, i)] \
                    + alpha \
                    * (next_reward + next_value - self.tuples[i][self.read_tuple(self.intermediate, i)])
            else:
                self.tuples[i][self.read_tuple(self.intermediate, i)] = 0

        # Permet d'observer les valeurs des poids et des ajouts de poids
        # print(self.tuples[i][self.read_tuple(self.intermediate, i)])
        # print(alpha * (next_reward + next_value - self.tuples[i][self.read_tuple(self.intermediate, i)]))

    def move_tiles_left(self, grid):
        """
        Déplace toutes les tuiles possibles vers la gauche de la grille
        :param grid: la grille sur laquelle la partie se déroule
        :return: le score obtenu après l'action
        """
        self.scoreL = 0
        for row in grid:
            row.sort(key=lambda x: 0 if x == 0 else 1, reverse=True)
            for i in range(3):
                if row[i] == row[i + 1]:
                    row[i] *= 2
                    self.scoreL += row[i]
                    row[i + 1] = 0
            row.sort(key=lambda x: 0 if x == 0 else 1, reverse=True)
        return self.scoreL

    def move_tiles_right(self, grid):
        """
        Déplace toutes les tuiles possibles vers la droite de la grille
        :param grid: la grille sur laquelle la partie se déroule
        :return: le score obtenu après l'action
        """
        self.scoreR = 0
        for row in grid:
            row.sort(key=lambda x: 0 if x == 0 else 1)
            for i in range(3, 0, -1):
                if row[i] == row[i - 1]:
                    row[i] *= 2
                    self.scoreR += row[i]
                    row[i - 1] = 0
            row.sort(key=lambda x: 0 if x == 0 else 1)
        return self.scoreR

    def move_tiles_up(self, grid):
        """
        Déplace toutes les tuiles possibles vers le haut de la grille
        :param grid: la grille sur laquelle la partie se déroule
        :return: le score obtenu après l'action
        """
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
        return self.scoreU

    def move_tiles_down(self, grid):
        """
        Déplace toutes les tuiles possibles vers le bas de la grille
        :param grid: la grille sur laquelle la partie se déroule
        :return: le score obtenu après l'action
        """
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
        return self.scoreD

    def read_tuple(self, grille, i):
        """
        Recuperation du poids associé à un tuple
        :param grille: la grille sur laquelle la partie se déroule
        :param i: le tuple pour lequel on cherche le poids
        :return: le poids associé au tuple d'entré
        """
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

    def draw(self):
        """
        Dessine la fenêtre de jeu
        """
        self.screen.fill((255, 255, 255))
        self.font = pygame.font.SysFont("Arial", 30)
        score_text = self.font.render("Score: " + str(self.score), True, (0, 0, 0))
        move_text = self.font.render("Move: " + str(self.moveNb), True, (0, 0, 0))
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
        """
        Lancement de la partie
        """
        if os.path.isfile('tuples2048_method3'):
            with open('tuples2048_method3', 'rb') as file:
                print("Lecture du fichier tuples2048_method3")
                if os.stat('tuples2048_method3').st_size > 0:
                    self.tuples = pickle.load(file)
        else:
            print("Erreur : Le fichier n'existe pas")
        self.draw()

        while not self.is_game_over():
            self.initial = self.grid_copy()
            self.reward = 0
            self.best_choice()
            self.intermediate = self.grid_copy()
            self.score += self.reward
            if self.grid != self.initial:
                self.moveNb = self.moveNb + 1
                self.add_new_tile()
                self.draw()
            if self.learn:
                self.learn_evaluation()
            pygame.time.wait(50)

        print("---------------")
        print("GAME OVER")
        print("Score : ", self.score)
        print("moveNb ", self.moveNb)
        print("Best tile :", self.best_tile())
        print("---------------\n")

        with open('tuples2048_method3', 'wb') as file:
            print("Mise à jour du fichier tuples2048_method3")
            pickle.dump(self.tuples, file)
        pygame.quit()
        quit()


game = game2048()
game.run()
