import heapq
import random
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

def a_star(puzzle, goal, heuristic):
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

def random_moves(puzzle, num_moves):
    directions = ['up', 'down', 'left', 'right']
    last_moves = []
    for _ in range(num_moves):
        possible_moves = [
            direction for direction in directions
            if puzzle.is_valid_move(direction)
        ]
        if not possible_moves:
            continue
        move = random.choice(possible_moves)
        while last_moves and move == last_moves[-1]:
            move = random.choice(possible_moves)
        puzzle.move(move)
        last_moves.append(move)
        if len(last_moves) > 2:
            last_moves.pop(0)
    return puzzle

def heuristic_one(puzzle, num_moves):
    # Implementação da Heurística 1 - Análise em um nível
    for _ in range(num_moves):
        best_move = None
        best_score = float('inf')
        for direction in ['up', 'down', 'left', 'right']:
            neighbor = Puzzle([row[:] for row in puzzle.board])
            neighbor.move(direction)
            score = heuristic(neighbor.board, generate_goal_board(puzzle.size))
            if score < best_score:
                best_score = score
                best_move = direction
        if best_move:
            puzzle.move(best_move)
    return puzzle

def heuristic_two(puzzle, num_moves):
    # Implementação da Heurística 2 - Análise em dois níveis
    for _ in range(num_moves):
        best_move = None
        best_score = float('inf')
        for direction in ['up', 'down', 'left', 'right']:
            neighbor = Puzzle([row[:] for row in puzzle.board])
            neighbor.move(direction)
            score = heuristic(neighbor.board, generate_goal_board(puzzle.size))
            for sub_direction in ['up', 'down', 'left', 'right']:
                sub_neighbor = Puzzle([row[:] for row in neighbor.board])
                sub_neighbor.move(sub_direction)
                sub_score = heuristic(sub_neighbor.board, generate_goal_board(puzzle.size))
                score += sub_score
            if score < best_score:
                best_score = score
                best_move = direction
        if best_move:
            puzzle.move(best_move)
    return puzzle

def personal_heuristic(puzzle, num_moves):
    # Implementação da Heurística Pessoal - Distância de Manhattan ponderada
    for _ in range(num_moves):
        best_move = None
        best_score = float('inf')
        for direction in ['up', 'down', 'left', 'right']:
            neighbor = Puzzle([row[:] for row in puzzle.board])
            neighbor.move(direction)
            score = 0
            for i in range(puzzle.size):
                for j in range(puzzle.size):
                    tile = neighbor.board[i][j]
                    if tile != 0:
                        goal_x, goal_y = find_position(generate_goal_board(puzzle.size), tile)
                        distance = abs(goal_x - i) + abs(goal_y - j)
                        score += distance * (tile ** 2)  # Ponderação pelo valor da peça
            if score < best_score:
                best_score = score
                best_move = direction
        if best_move:
            puzzle.move(best_move)
    return puzzle

def generate_goal_board(size):
    return [list(range(i*size+1, (i+1)*size+1)) for i in range(size)]