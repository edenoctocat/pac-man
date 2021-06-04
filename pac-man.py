import os
from time import sleep
# import curses
# import keyboard
import getch
import sys

class Field:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.field = [['. ' for i in range(self.width)] for i in range(self.height)]
		self.generate_maze()

	def generate_maze(self):
		pass # self.field

	def clear(self):
		self.field = [['. ' for i in range(self.width)] for i in range(self.height)]
		self.screen = list(self.field)

	def render(self, pacman_location):
		self.clear()
		x = pacman_location[0]
		y = pacman_location[1]
		self.screen[x][y] = 'O '
		print(self.field)
		print(self.screen)

	def display(self):
		print('\n'.join([''.join(row) for row in self.screen]))

class Pacman:
	def __init__(self, field):
		self.position = [0, 0]
		self.direction = 'd'
		self.field = field

	def check_position(self, location):
		if location[0] > 9 or location[1] > 9 or location[0] < 0 or location[1] < 0:
			return False
		elif self.field[location[0]][location[1]] == '_ ' or self.field[location[0]][location[1]] == '| ':
			return False
		else:
			return True

	def set_direction(self, key):
		self.direction = key

	def move(self):
		new_position = list(self.position)
    
		if self.direction == 'w':
			new_position[0] -= 1
		elif self.direction == 's':
			new_position[0] += 1
		elif self.direction == 'a':
			new_position[1] -= 1
		elif self.direction == 'd':
			new_position[1] += 1
    
		if self.check_position(new_position):
			self.position = list(new_position)
		else:
			pass

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
	field = Field(15, 20)
	pacman = Pacman(field.field)
	field.render(pacman.position)
	field.display()

	# keyboard.add_hotkey('up', lambda: pacman.set_direction('up'))
	# keyboard.add_hotkey('down', lambda: pacman.set_direction('down'))
	# keyboard.add_hotkey('left', lambda: pacman.set_direction('left'))
	# keyboard.add_hotkey('right', lambda: pacman.set_direction('right'))

	ch = getch.getch()

	while ch != 'q':
		os.system('clear')
		pacman.set_direction(ch)
		pacman.move()
		field.render(pacman.position)
		field.display()
		ch = getch.getch()
		sleep(.3)

main()
