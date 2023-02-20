# GIRAUD-RENARD Benjamin et beaucoup de ChatGPT

import random
import pygame
import copy

class game2048():
	def __init__(self):
		# grille complète
		self.grid = [
				[0,0,0,0],
				[0,0,0,0],
				[0,0,0,0],
				[0,0,0,0],
				]

		self.tilesColor = {
			0:"#BFB3A5",
			2:"#FAE7E0",
			4:"#FAE5CA",
			8:"#FBB17A",
			16:"#DF9F74",
			32:"#E08A72",
			64:"#FD5B42",
			128:"#FAD177",
			256:"#F7D067",
			512:"#F9CA58",
			1024:"#F9CA58",
			2048:"#FBC52D",
			4096:"#F66574",
			8192:"#F34B5C",
			16384:"#EB4039",
			32768:"#70B3D8",
			65536:"#5EA1E4",
			131072:"#007FC2"
		}
		self.score = 0
		self.nbMove = 0
		self.add_new_tile()
		self.add_new_tile()

		pygame.init()
		self.font = pygame.font.SysFont("Arial", 36)
		self.screen = pygame.display.set_mode((400, 500))
		pygame.display.set_caption("2048 Game")

	def add_new_tile(self):
		empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
		if empty_cells:
			i, j = random.choice(empty_cells)
			self.grid[i][j] = 2 if random.random() < 0.9 else 4

	def move_tiles_left(self):
		for row in self.grid:
			row.sort(key=lambda x: 0 if x == 0 else 1, reverse=True)
			for i in range(3):
				if row[i] == row[i+1]:
					row[i] *= 2
					self.score += row[i]
					row[i+1] = 0
			row.sort(key=lambda x: 0 if x == 0 else 1, reverse=True)

	def move_tiles_right(self):
		for row in self.grid:
			row.sort(key=lambda x: 0 if x == 0 else 1)
			for i in range(3, 0, -1):
				if row[i] == row[i-1]:
					row[i] *= 2
					self.score += row[i]
					row[i-1] = 0
			row.sort(key=lambda x: 0 if x == 0 else 1)

	def move_tiles_up(self):
		for j in range(4):
			col = [self.grid[i][j] for i in range(4)]
			col.sort(key=lambda x: 0 if x == 0 else 1, reverse=True)
			for i in range(3):
				if col[i] == col[i+1]:
					col[i] *= 2
					self.score += col[i]
					col[i+1] = 0
			col.sort(key=lambda x: 0 if x == 0 else 1, reverse=True)
			for i in range(4):
				self.grid[i][j] = col[i]

	def move_tiles_down(self):
		for j in range(4):
			col = [self.grid[i][j] for i in range(4)]
			col.sort(key=lambda x: 0 if x == 0 else 1)
			for i in range(3, 0, -1):
				if col[i] == col[i-1]:
					col[i] *= 2
					self.score += col[i]
					col[i-1] = 0
			col.sort(key=lambda x: 0 if x == 0 else 1)
			for i in range(4):
				self.grid[i][j] = col[i]

	def is_game_over(self):
		empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
		if empty_cells: return False
		for i in range(3):
			for j in range(3):
				if self.grid[i][j] == self.grid[i+1][j] or self.grid[i][j] == self.grid[i][j+1]:
					return False
		# Check the last row and column separately
		for i in range(3):
			if self.grid[3][i] == self.grid[3][i+1]:
				return False
			if self.grid[i][3] == self.grid[i+1][3]:
				return False
		return True

	def best_tile(self):
		maxTile = self.grid[0][0]
		for i in range(4):
			for j in range(4):
				if self.grid[i][j] > maxTile: maxTile = self.grid[i][j]
		return maxTile

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
					size = 0 if len(str(self.grid[i][j]))-4 < 0 else len(str(self.grid[i][j]))-3
					self.font = pygame.font.SysFont("Arial", 32 - 4 * size)
					text = self.font.render(str(self.grid[i][j]), True, (0, 0, 0))
					text_rect = text.get_rect()
					text_rect.center = (j * 100 + 50, i * 100 + 150)
					self.screen.blit(text, text_rect)
		pygame.display.update()

	def run(self):
		self.draw()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

				if event.type == pygame.KEYDOWN and event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
					saveGrid = copy.deepcopy(self.grid)
					if event.key == pygame.K_LEFT:
						self.move_tiles_left()
					elif event.key == pygame.K_RIGHT:
						self.move_tiles_right()
					elif event.key == pygame.K_UP:
						self.move_tiles_up()
					elif event.key == pygame.K_DOWN:
						self.move_tiles_down()
					if self.grid != saveGrid: 
						self.nbMove+=1
						self.add_new_tile()
						self.draw()

				if self.is_game_over():
					print("---------------")
					print("GAME OVER")
					print("Meilleure tuile : ", self.best_tile())
					print("Score : ", self.score)
					print("NbMove ", self.nbMove)
					print("---------------\n")
					pygame.quit()
					quit()
			pygame.time.wait(50)

game = game2048()
game.run()