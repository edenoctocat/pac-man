import os
from time import sleep
import getch
import sys
import random

class Field:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.score = 0
		self.field = []
		self.generate_maze()

	def generate_maze(self):
		f = open('maze.txt', 'r')
		for y in range(20):
			line = f.readline()
			line_list = []
			for x in range(0, len(line), 2):
				line_list.append(line[x:x+2])
			self.field.append(line_list)
		f.close()

	def render(self, pacman_position, pacman_prev_position, ghost_positions, ghost_prev_positions, ghost_prev_dots):
		if self.field[pacman_position[0]][pacman_position[1]] == '. ':
			self.score += 10 
		self.field[pacman_prev_position[0]][pacman_prev_position[1]] = '  '
		self.field[pacman_position[0]][pacman_position[1]] = 'O '
		for prev_position, prev_dot in zip(ghost_prev_positions, ghost_prev_dots):
			if prev_dot == True:
				self.field[prev_position[0]][prev_position[1]] = '. '
			else:
				self.field[prev_position[0]][prev_position[1]] = '  '				
		for position in ghost_positions:
			self.field[position[0]][position[1]] = '& '

	def display(self):
		print('score:', self.score)
		print(''.join([''.join(row) for row in self.field]))

	def check_if_pacman_eaten(self):
		for line in self.field:
			for pixel in line:
				if pixel == 'O ':
					return 'continue'
		return 'game over'

class Pacman:
	def __init__(self, maze):
		self.position = [15, 7]
		self.prev_position = [15, 7]
		self.direction = 'd'
		self.status = 'alive'
		self.maze = maze

	def check_position(self, position):
		if position[0] > 18 or position[1] > 14 or position[0] < 0 or position[1] < 0:
			return False
		elif self.maze[position[0]][position[1]] == '__' or self.maze[position[0]][position[1]] == '| ' or self.maze[position[0]][position[1]] == '|-' or self.maze[position[0]][position[1]] == '- ' or self.maze[position[0]][position[1]] == '--' or self.maze[position[0]][position[1]] == '|_' or self.maze[position[0]][position[1]] == ' _' or self.maze[position[0]][position[1]] == '_ ':
			return False
		else:
			return True

	def set_direction(self, key):
		self.direction = key

	def move(self):
		self.prev_position = list(self.position)
    
		if self.direction == 'w':
			self.position[0] -= 1
		elif self.direction == 's':
			self.position[0] += 1
		elif self.direction == 'a':
			self.position[1] -= 1
		elif self.direction == 'd':
			self.position[1] += 1
    
		if self.check_position(self.position):
			pass
		else:
			self.position = list(self.prev_position)

class Ghost:
	def __init__(self, maze, position):
		self.position = position
		self.prev_position = position
		self.direction = 'd'
		self.maze = maze
		self.current_dot = False
		self.prev_dot = False

	def start(self, new_position):
		self.position = list(new_position)

	def check_position(self, position):
		if position[0] > 18 or position[1] > 14 or position[0] < 0 or position[1] < 0:
			return False
		elif self.maze[position[0]][position[1]] == '__' or self.maze[position[0]][position[1]] == '| ' or self.maze[position[0]][position[1]] == '|-' or self.maze[position[0]][position[1]] == '- ' or self.maze[position[0]][position[1]] == '--' or self.maze[position[0]][position[1]] == '|_' or self.maze[position[0]][position[1]] == ' _' or self.maze[position[0]][position[1]] == '_ ':
			return False
		else:
			return True

	def set_direction(self, directions):
		self.direction = random.choice(directions)

	def find_dot(self, field):
		if field[self.position[0]][self.position[1]] == '. ':
			self.current_dot = True
		else:
			self.current_dot = False

	def move(self):
		self.prev_position = list(self.position)
		self.update_position()

		while self.check_position(self.position) == False:
			directions = ['w', 'a', 's', 'd']
			directions.remove(self.direction)
			self.set_direction(directions)
			self.update_position()

		directions = ['w', 'a', 's', 'd']
		directions.remove(self.opp_direction)    
		self.set_direction(directions)
		self.prev_dot = bool(self.current_dot)


	def update_position(self):
		self.position = list(self.prev_position)
		if self.direction == 'w':
			self.position[0] -= 1
			self.opp_direction = 's'
		elif self.direction == 's':
			self.position[0] += 1
			self.opp_direction = 'w'
		elif self.direction == 'a':
			self.position[1] -= 1
			self.opp_direction = 'd'
		elif self.direction == 'd':
			self.position[1] += 1
			self.opp_direction = 'a'


def main():
	os.system('clear')
	f = open('opening_text.txt', 'r')
	for i in range(3):
		os.system('clear')
		print(f.read())
		f.seek(0)
		print('\n' + (' ' * 36) + ('. ' * (i%3)) + 'O ' + ('. ' * (2 - i%3)))
		sleep(.5)
	f.close()

	os.system('clear')
	field = Field(15, 19)
	pacman = Pacman(field.field)
	inky = Ghost(field.field, [9, 6])
	pinky = Ghost(field.field, [9, 8])
	blinky = Ghost(field.field, [10, 6])
	clyde = Ghost(field.field, [10, 8])
	ghosts = [inky, pinky, blinky, clyde]
	field.render(pacman.position, pacman.prev_position, [inky.position, pinky.position, blinky.position, clyde.position], [inky.prev_position, pinky.prev_position, blinky.prev_position, clyde.prev_position], [inky.prev_dot, pinky.prev_dot, blinky.prev_dot, clyde.prev_dot])
	field.display()

	print('\npress w to move up. \npress s to move down. \npress a to move left. \npress d to move right. \n\npress q to quit. \npress h for help.')
	print('\npress any key to continue...')

	rounds = 0
	ch = getch.getch()	

	while ch != 'q':
		os.system('clear')
		pacman.set_direction(ch)
		pacman.move()

		for ghost in ghosts:
			ghost.move()
			ghost.find_dot(field.field)

		if rounds == 2:
			inky.start([0, 0])
		elif rounds == 4:
			pinky.start([0, 14])
		elif rounds == 6:
			blinky.start([18, 0])
		elif rounds == 8:
			clyde.start([18, 14])

		field.render(pacman.position, pacman.prev_position, [inky.position, pinky.position, blinky.position, clyde.position], [inky.prev_position, pinky.prev_position, blinky.prev_position, clyde.prev_position], [inky.prev_dot, pinky.prev_dot, blinky.prev_dot, clyde.prev_dot])
		field.display()
		if field.check_if_pacman_eaten() == 'game over':
			f = open('game_over.txt', 'r')
			print(f.read())
			f.close()
			sys.exit()

		if ch == 'h':
			print('\npress w to move up. \npress s to move down. \npress a to move left. \npress d to move right. \n\npress h for help. \npress q to quit.')
			print('\npress any key to continue...')

		ch = getch.getch()
		sleep(.2)
		rounds += 1

main()
