import random
from puzzle.board import Puzzle

def find_position(board, value):
    for i, row in enumerate(board):
        if value in row:
            return i, row.index(value)
    return None

def random_solver(puzzle):
    num_moves = 0
    last_moves = []
    while puzzle.board != generate_goal_board(puzzle.size):
        possible_moves = [
            direction for direction in ['up', 'down', 'left', 'right']
            if puzzle.is_valid_move(direction)
        ]
        if not possible_moves:
            break
        move = random.choice(possible_moves)

        if last_moves and move == last_moves[-1]:
            continue

        puzzle.move(move)
        num_moves += 1
        last_moves.append(move)
        if len(last_moves) > 2:
            last_moves.pop(0)
            
    return num_moves

def heuristic_one_solver(puzzle):
    goal = generate_goal_board(puzzle.size)
    num_moves = 0
    last_moves = []

    while puzzle.board != goal:
        best_move = None
        min_distance = float('inf')

        for move in ['up', 'down', 'left', 'right']:
            if puzzle.is_valid_move(move):
                neighbor = Puzzle([row[:] for row in puzzle.board])
                neighbor.move(move)
                distance = heuristic_one(neighbor, goal)
                if distance < min_distance:
                    min_distance = distance
                    best_move = move

        if best_move:
            puzzle.move(best_move)
            num_moves += 1
            last_moves.append(best_move)
            if len(last_moves) > 2:
                last_moves.pop(0)

    return num_moves

def heuristic_one(puzzle, goal):
    size = len(puzzle.board)
    distance = 0
    for i in range(size):
        for j in range(size):
            tile = puzzle.board[i][j]
            if tile != 0:
                goal_x, goal_y = find_position(goal, tile)
                distance += abs(goal_x - i) + abs(goal_y - j)
    return distance

def heuristic_two_solver(puzzle):
    goal = generate_goal_board(puzzle.size)
    num_moves = 0

    last_moves = []

    while puzzle.board != goal:
        best_move = None
        min_distance = float('inf')

        for move in ['up', 'down', 'left', 'right']:
            if puzzle.is_valid_move(move):
                neighbor = Puzzle([row[:] for row in puzzle.board])
                neighbor.move(move)
                distance = heuristic_two(neighbor, goal)

                if distance < min_distance:
                    min_distance = distance
                    best_move = move
        
        if best_move and (not last_moves or best_move != last_moves[-1]):
            puzzle.move(best_move)
            num_moves += 1
            last_moves.append(best_move)
            if len(last_moves) > 2:
                last_moves.pop(0)

    return num_moves

def heuristic_two(puzzle, goal):
    best_move = None
    min_distance = float('inf')

    for move1 in ['up', 'down', 'left', 'right']:
        neighbor = Puzzle([row[:] for row in puzzle.board])
        if neighbor.move(move1):
            for move2 in ['up', 'down', 'left', 'right']:
                sub_neighbor = Puzzle([row[:] for row in neighbor.board])
                if sub_neighbor.move(move2):
                    distance = heuristic_one(sub_neighbor, goal)
                    if distance < min_distance:
                        min_distance = distance
                        best_move = move1

    return best_move

def personal_heuristic_solver(puzzle):
    goal = generate_goal_board(puzzle.size)
    num_moves = 0
    last_moves = []

    while puzzle.board != goal:
        best_move = None
        min_distance = float('inf')

        for move in ['up', 'down', 'left', 'right']:
            if puzzle.is_valid_move(move):
                neighbor = Puzzle([row[:] for row in puzzle.board])
                neighbor.move(move)
                distance = personal_heuristic(neighbor.board, goal)
                
                if distance < min_distance:
                    min_distance = distance
                    best_move = move

        if best_move:
            puzzle.move(best_move)
            num_moves += 1
            last_moves.append(best_move)
            if len(last_moves) > 2:
                last_moves.pop(0)

    return num_moves

def personal_heuristic(board, goal):
    distance = 0
    size = len(board)
    misplaced_penalty = 0

    for i in range(size):
        for j in range(size):
            tile = board[i][j]
            if tile != 0:
                goal_x, goal_y = find_position(goal, tile)
                distance += abs(goal_x - i) + abs(goal_y - j)
                if (goal_x, goal_y) != (i, j):
                    misplaced_penalty += 1

    return distance + misplaced_penalty
        
def generate_goal_board(size):
    board = list(range(1, size*size)) + [0]
    return [board[i*size:(i+1)*size] for i in range(size)]