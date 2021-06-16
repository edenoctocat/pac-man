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

	def render(self, pacman_position, pacman_prev_position):
		if self.field[pacman_position[0]][pacman_position[1]] == '. ':
			self.score += 10 
		self.field[pacman_prev_position[0]][pacman_prev_position[1]] = '  '
		self.field[pacman_position[0]][pacman_position[1]] = 'O '

	def display(self):
		print('score:', self.score)
		print(''.join([''.join(row) for row in self.field]))

class Pacman:
	def __init__(self, maze):
		self.position = [15, 7]
		self.prev_position = [15, 7]
		self.direction = 'd'
		self.maze = maze

	def check_position(self, position):
		if position[0] > 19 or position[1] > 14 or position[0] < 0 or position[1] < 0:
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
	def __init__(self):
		pass

def main():
	os.system('clear')
	f = open('opening_text1.txt', 'r')
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
	field.render(pacman.position, pacman.prev_position)
	field.display()

	print('\npress w to move up. press s to move down. press a to move left. press d to move right. press q to quit.')
	print('press any key to continue')

	ch = getch.getch()

	while ch != 'q':
		os.system('clear')
		pacman.set_direction(ch)
		pacman.move()
		field.render(pacman.position, pacman.prev_position)
		field.display()
		ch = getch.getch()
		sleep(.2)

main()
