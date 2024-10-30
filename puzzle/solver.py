import heapq
from puzzle.board import Puzzle 

def find_position(board, value):
    for i, row in enumerate(board):
        if value in row:
            return i, row.index(value)
    return None

def heuristic(board, goal):
    size = len(board)
    distance = 0
    for i in range(size):
        for j in range(size):
            tile = board[i][j]
            if tile != 0:
                goal_x, goal_y = find_position(goal, tile)
                distance += abs(goal_x - i) + abs(goal_y - j)
    return distance

def a_star(puzzle, goal):
    open_set = []
    heapq.heappush(open_set, (0, puzzle))
    came_from = {}
    g_score = {str(puzzle.board): 0}
    f_score = {str(puzzle.board): heuristic(puzzle.board, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current.board == goal:
            return reconstruct_path(came_from, current)

        for direction in ['up', 'down', 'left', 'right']:
            neighbor = Puzzle([row[:] for row in current.board])
            neighbor.move(direction)
            tentative_g_score = g_score[str(current.board)] + 1

            if str(neighbor.board) not in g_score or tentative_g_score < g_score[str(neighbor.board)]:
                came_from[str(neighbor.board)] = current
                g_score[str(neighbor.board)] = tentative_g_score
                f_score[str(neighbor.board)] = tentative_g_score + heuristic(neighbor.board, goal)
                heapq.heappush(open_set, (f_score[str(neighbor.board)], neighbor))

    return None

def reconstruct_path(came_from, current):
    total_path = [current]
    while str(current.board) in came_from:
        current = came_from[str(current.board)]
        total_path.append(current)
    return total_path[::-1]