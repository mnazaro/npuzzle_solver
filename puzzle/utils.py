def manhattan_distance(board, goal):
    distance = 0
    size = len(board)
    for i in range(size):
        for j in range(size):
            tile = board[i][j]
            if tile != 0:
                goal_x, goal_y = divmod(goal.index(tile), size)
                distance += abs(goal_x - i) + abs(goal_y - j)
    return distance