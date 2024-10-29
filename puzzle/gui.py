import tkinter as tk
from puzzle.board import Puzzle
from puzzle.solver import a_star
import random

class PuzzleGUI:
    def __init__(self, root, puzzle):
        self.root = root
        self.puzzle = puzzle
        self.buttons = []
        self.create_widgets()
        self.update_board()

    def create_widgets(self):
        self.root.title("8 Puzzle Game")

        # Título
        title = tk.Label(self.root, text="8 Puzzle Game", font=("Helvetica", 16))
        title.grid(row=0, columnspan=self.puzzle.size)

        # Instruções
        instructions = tk.Label(self.root, text="Clique nos botões para mover as peças.", font=("Helvetica", 10))
        instructions.grid(row=1, column=0, columnspan=self.puzzle.size)

        # Botões do tabuleiro
        for i in range(self.puzzle.size):
            row = []
            for j in range(self.puzzle.size):
                button = tk.Button(self.root, text='', width=4, height=2, font=("Helvetica", 14),
                                   bg='lightblue', fg='black', relief='raised', bd=3,
                                   command=lambda i=i, j=j: self.move_tile(i, j))
                button.grid(row=i+2, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)

        # Botão de reset
        reset_button = tk.Button(self.root, text="Reset", command=self.reset_board, font=("Helvetica", 12),
                                 bg='lightgreen', fg='black', relief='raised', bd=3)
        reset_button.grid(row=self.puzzle.size+2, column=0, columnspan=self.puzzle.size//2)

        # Botão de resolver automaticamente
        solve_button = tk.Button(self.root, text="Solve", command=self.solve_puzzle, font=("Helvetica", 12),
                                 bg='lightcoral', fg='black', relief='raised', bd=3)
        solve_button.grid(row=self.puzzle.size+2, column=self.puzzle.size//2, columnspan=self.puzzle.size//2)

    def update_board(self):
        for i in range(self.puzzle.size):
            for j in range(self.puzzle.size):
                tile = self.puzzle.board[i][j]
                self.buttons[i][j].config(text=str(tile) if tile != 0 else '')

    def move_tile(self, i, j):
        x, y = self.puzzle.empty_tile
        if (i == x and abs(j - y) == 1) or (j == y and abs(i - x) == 1):
            self.puzzle.move('up' if i < x else 'down' if i > x else 'left' if j < y else 'right')
            self.update_board()

    def reset_board(self):
        self.puzzle = Puzzle(generate_random_board(self.puzzle.size))
        self.update_board()

    def solve_puzzle(self):
        goal_board = generate_goal_board(self.puzzle.size)
        solution = a_star(self.puzzle, goal_board)
        if solution:
            for step in solution:
                self.puzzle = step
                self.update_board()
                self.root.update()
                self.root.after(500)  # Delay para visualizar os passos

def generate_random_board(size):
    board = list(range(size*size))
    random.shuffle(board)
    return [board[i*size:(i+1)*size] for i in range(size)]

def generate_goal_board(size):
    return [list(range(i*size+1, (i+1)*size+1)) for i in range(size)]

def choose_size():
    size_window = tk.Tk()
    size_window.title("Escolha o tamanho do tabuleiro")

    tk.Label(size_window, text="Escolha o tamanho do tabuleiro (3-10):", font=("Helvetica", 12)).pack(pady=10)
    size_var = tk.IntVar(value=3)
    size_entry = tk.Entry(size_window, textvariable=size_var, font=("Helvetica", 12))
    size_entry.pack(pady=10)

    def start_game():
        size = size_var.get()
        if 3 <= size <= 10:
            size_window.destroy()
            initial_board = generate_random_board(size)
            puzzle = Puzzle(initial_board)
            root = tk.Tk()
            gui = PuzzleGUI(root, puzzle)
            root.mainloop()
        else:
            tk.Label(size_window, text="Tamanho inválido. Tente novamente.", font=("Helvetica", 12)).pack(pady=10)
    
    tk.Button(size_window, text="Começar", command=start_game, font=("Helvetica", 12)).pack(pady=10)
    size_window.mainloop()

def main():
    choose_size()

if __name__ == "__main__":
    main()