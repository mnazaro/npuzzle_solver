class Puzzle:
    def __init__(self, board):
        self.board = board
        self.size = len(board)
        self.empty_tile = self.find_empty_tile()

    def find_empty_tile(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def display(self):
        for row in self.board:
            print(' '.join(str(tile) if tile != 0 else ' ' for tile in row))
        print()

    def move(self, direction):
        x, y = self.empty_tile
        if direction == 'up' and x > 0:
            self.board[x][y], self.board[x-1][y] = self.board[x-1][y], self.board[x][y]
            self.empty_tile = (x-1, y)
        elif direction == 'down' and x < self.size - 1:
            self.board[x][y], self.board[x+1][y] = self.board[x+1][y], self.board[x][y]
            self.empty_tile = (x+1, y)
        elif direction == 'left' and y > 0:
            self.board[x][y], self.board[x][y-1] = self.board[x][y-1], self.board[x][y]
            self.empty_tile = (x, y-1)
        elif direction == 'right' and y < self.size - 1:
            self.board[x][y], self.board[x][y+1] = self.board[x][y+1], self.board[x][y]
            self.empty_tile = (x, y+1)
        else:
            print("Movimento inválido!")

    def is_valid_move(self, direction):
        x, y = self.empty_tile
        return (direction == 'up' and x > 0) or (direction == 'down' and x < self.size - 1) or (direction == 'left' and y > 0) or (direction == 'right' and y < self.size - 1)