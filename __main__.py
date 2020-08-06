import pygame
pygame.font.init()
from spot import Spot
from algorithms import astar_algorithm
from algorithms import bfs
from algorithms import make_borders
from algorithms import best_first_search
from button import Button
from constants import *

def make_grid(rows, width, maze=False):
	#If maze wanted return a grid that has a random maze produced by prims algorithm
	if maze:
		return make_borders(rows, width)

	#Else return an grid of white spots
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows+1):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width, buttons):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)
	draw_buttons(win, buttons)
	draw_grid(win, rows, width)

	pygame.display.update()

def draw_buttons(win, buttons):
	font = pygame.font.Font('freesansbold.ttf',15)
	display = font.render('Algorithms',True,BLACK)
	textRect = display.get_rect()
	textRect.topleft = (30,WIDTH+10)
	WIN.blit(display,textRect)
	for button in buttons:
		button.draw(win)

	font = pygame.font.Font('freesansbold.ttf',10)
	display = font.render('Select an Algorithm to the left, first click places the start node',True,BLACK)
	textRect = display.get_rect()
	textRect.topleft = (150,WIDTH+30)
	WIN.blit(display,textRect)

	display = font.render('Second click places the end node and any clicks after that place barriers',True,BLACK)
	textRect = display.get_rect()
	textRect.topleft = (150,WIDTH+40)
	WIN.blit(display,textRect)

	display = font.render('Press Space to visualize and c to reset',True,BLACK)
	textRect = display.get_rect()
	textRect.topleft = (150,WIDTH+50)
	WIN.blit(display,textRect)

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def update_buttons(buttons, pos):
	for button in buttons:
		if button.contains(pos):
			button.selected = True
			if button == buttons[0]:
				buttons[1].selected = False
				buttons[2].selected = False
				return 'astar'

			elif button == buttons[1]:
				buttons[0].selected = False
				buttons[2].selected = False
				return 'dijkstras'

			elif button == buttons[2]:
				buttons[0].selected = False
				buttons[1].selected = False
				return 'best_first'


def main(win, width):
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True

	algo = 'astar'

	astar_button = Button((10, WIDTH+30, 110, 20), 'Astar Algorithm')
	astar_button.selected = True
	dijkstra_button = Button((10, WIDTH+50, 110, 20), 'Dijkstras Algorithm')
	best_first_button = Button((10, WIDTH+70, 110, 20), 'Best-First-Search')
	buttons = [astar_button, dijkstra_button, best_first_button]
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				if pos[1]<=width:
					row, col = get_clicked_pos(pos, ROWS, width)
					spot = grid[row][col]
					if not start and spot != end:
						start = spot
						start.make_start()

					elif not end and spot != start:
						end = spot
						end.make_end()

					elif spot != end and spot != start:
						spot.make_barrier()
				else:
					algo = update_buttons(buttons, pos)

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					if algo == 'astar':
						for row in grid:
							for spot in row:
								spot.update_neighbors(grid)
						astar_algorithm(lambda: draw(win, grid, ROWS, width, buttons), grid, start, end)
					elif algo == 'dijkstras':
						for row in grid:
							for spot in row:
								spot.update_neighbors(grid)
						bfs(lambda: draw(win, grid, ROWS, width, buttons), grid, start, end)
					elif algo == 'best_first':
						for row in grid:
							for spot in row:
								spot.update_neighbors(grid)
						best_first_search(lambda: draw(win, grid, ROWS, width, buttons), grid, start, end)
				if event.key == pygame.K_m:
					start = None
					end = None
					grid = make_grid(ROWS, width, True)
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

		draw(win, grid, ROWS, width, buttons)
		pygame.display.update()

	pygame.quit()

pygame.display.set_caption("Path Finding Algorithm Visualization")
main(WIN, WIDTH)
