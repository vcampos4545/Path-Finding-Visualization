import pygame
from queue import PriorityQueue
from spot import Spot

def make_borders(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		if i == 0 or i == rows - 1:
			temp = []
			for j in range(rows):
				spot = Spot(i, j, gap, rows)
				spot.make_barrier()
				temp.append(spot)
			grid.append(temp)
		else:
			spot = Spot(i, 0, gap, rows)
			spot.make_barrier()
			temp = [spot]
			for j in range(1, rows-1):
				temp.append(Spot(i, j, gap, rows))
			spot = Spot(i, rows-1, gap, rows)
			spot.make_barrier()
			temp.append(spot)
			grid.append(temp)

	return grid


def astar_algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			start.make_start()
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def best_first_search(draw, grid, start, end):
	open_set = PriorityQueue()
	open_set.put((0, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		#Handle Quiting
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		#Get current node and remove it from the open_set_has
		current = open_set.get()[1]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			start.make_start()
			end.make_end()
			return True

		min_f_score = float("inf")
		min_spot = None
		for neighbor in current.neighbors:
			if not neighbor.is_closed():
				temp_f_score = g_score[current] + 1 + h(neighbor.get_pos(), end.get_pos())
				if temp_f_score < min_f_score:
					g_score[neighbor] = g_score[current] + 1
					f_score[neighbor] = temp_f_score
					came_from[neighbor] = current
					min_f_score = temp_f_score
					min_spot = neighbor
		open_set.put((f_score[min_spot], min_spot))
		open_set_hash.add(min_spot)
		min_spot.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def bfs(draw, grid, start, end):
	visited = []
	open_set = PriorityQueue()
	open_set.put((0, start))
	came_from = {}
	open_set_hash = {start}
	dist = {spot: float("inf") for row in grid for spot in row}
	dist[start] = 0

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[1]
		open_set_hash.remove(current)
		visited.append(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			start.make_start()
			end.make_end()
			return True

		for neighbor in current.neighbors:

			current_dist = dist[current]
			neighbor_dist = current_dist + 1

			if neighbor not in open_set_hash and neighbor not in visited:
				dist[neighbor] = neighbor_dist
				open_set.put((neighbor_dist, neighbor))
				open_set_hash.add(neighbor)
				came_from[neighbor] = current
				neighbor.make_open()
			elif neighbor_dist < dist[neighbor]:
				dist[neighbor] = neighbor_dist
				came_from[neighbor] = current

		draw()

		if current != start:
			current.make_closed()

	return False

"""
Helpers
"""
def h(p1, p2):
	"""
	Heuristic Function Used in the A star algorithm
	"""
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()
