import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QGridLayout
from PySide6.QtWidgets import QSpinBox, QDialog, QDialogButtonBox
from PySide6.QtCore import Qt, QTimer, QRect, QPropertyAnimation
from puzzle.solver import random_solver, heuristic_one_solver, heuristic_two_solver, personal_heuristic_solver
from puzzle.board import Puzzle

class PuzzleGUI(QMainWindow):
    def __init__(self, puzzle):
        super().__init__()
        self.puzzle = puzzle
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Slide Puzzle Game")
        self.setGeometry(100, 100, 400, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        self.title = QLabel("Slide Puzzle Game")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 24px;")
        self.layout.addWidget(self.title)

        self.instructions = QLabel("Clique nos botões para mover as peças.")
        self.instructions.setAlignment(Qt.AlignCenter)
        self.instructions.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.instructions)

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.buttons = []
        for i in range(self.puzzle.size):
            row = []
            for j in range(self.puzzle.size):
                button = QPushButton('')
                button.setFixedSize(80, 80)
                button.setStyleSheet("font-size: 18px; background-color: #f8f8f8; color: #333;")
                button.clicked.connect(lambda _, i=i, j=j: self.move_tile(i, j))
                self.grid_layout.addWidget(button, i, j)
                row.append(button)
            self.buttons.append(row)

        self.reset_button = QPushButton("Reiniciar")
        self.reset_button.clicked.connect(self.reset_board)
        self.layout.addWidget(self.reset_button)

        self.solve_button = QPushButton("Resolver")
        self.solve_button.clicked.connect(self.solve_puzzle)
        self.layout.addWidget(self.solve_button)

        self.results_label = QLabel("")
        self.results_label.setAlignment(Qt.AlignCenter)
        self.results_label.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.results_label)

        self.update_board()

    def update_board(self):
        goal_board = generate_goal_board(self.puzzle.size)
        for i in range(self.puzzle.size):
            for j in range(self.puzzle.size):
                tile = self.puzzle.board[i][j]
                color = "#90ee90" if tile != 0 and tile == goal_board[i][j] else "#ff817e"
                self.buttons[i][j].setText(str(tile) if tile != 0 else '')
                self.buttons[i][j].setStyleSheet(
                    f"font-size: 18px; background-color: {color}; color: #333;" if tile != 0 else "font-size: 18px; background-color: lightgrey;")
    
    def solve_puzzle(self):
        self.solve_dialog = SolveDialog()
        if self.solve_dialog.exec() == QDialog.Accepted:
            mode = self.solve_dialog.get_mode()

            if mode == "random":
                num_moves = random_solver(self.puzzle)
                self.results_label.setText(f"Resolvido em {num_moves} movimentos.\n Utilizando movimentos aleatórios.")
            elif mode == "heuristic1":
                num_moves = heuristic_one_solver(self.puzzle)
                self.results_label.setText(f"Resolvido em {num_moves} movimentos.\n Utilizando a heurística 1.")
            elif mode == "heuristic2":
                num_moves = heuristic_two_solver(self.puzzle)
                self.results_label.setText(f"Resolvido em {num_moves} movimentos.\n Utilizando a heurística 2.")
            elif mode == "custom":
                num_moves = personal_heuristic_solver(self.puzzle)
                self.results_label.setText(f"Resolvido em {num_moves} movimentos.\n Utilizando a heurística personalizada.")
            self.update_board()

    def move_tile(self, i, j):
        x, y = self.puzzle.empty_tile
        if (i == x and abs(j - y) == 1) or (j == y and abs(i - x) == 1):
            direction = 'up' if i < x else 'down' if i > x else 'left' if j < y else 'right'
            self.puzzle.move(direction)
            self.update_board()

    def reset_board(self): # Reseta o tabuleiro, misturando as peças
        self.moves_dialog = MovesDialog()
        if self.moves_dialog.exec() == QDialog.Accepted:
            num_moves = self.moves_dialog.get_moves()
            self.puzzle = Puzzle(generate_goal_board(self.puzzle.size))
            self.random_moves(num_moves)
        self.update_board()


    def random_moves(self, num_moves): # Movimento aleatórios para misturar o tabuleiro
        directions = ['up', 'down', 'left', 'right']
        last_moves = []
        for _ in range(num_moves):
            possible_moves = [
                direction for direction in directions
                if self.puzzle.is_valid_move(direction)
            ]
            if not possible_moves:
                continue
            move = random.choice(possible_moves)
            while last_moves and move == last_moves[-1]:
                move = random.choice(possible_moves)
            self.puzzle.move(move)
            last_moves.append(move)
            if len(last_moves) > 2:
                last_moves.pop(0)
            self.update_board()

def generate_goal_board(size):
    board = list(range(1, size*size)) + [0]
    return [board[i*size:(i+1)*size] for i in range(size)]

# //MARK:- Dialogs

class SizeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Escolha o Tamanho do Tabuleiro")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Escolha o tamanho do tabuleiro (3-10):")
        self.layout.addWidget(self.label)

        self.spin_box = QSpinBox()
        self.spin_box.setRange(3, 10)
        self.spin_box.setValue(3)
        self.layout.addWidget(self.spin_box)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def get_size(self):
        return self.spin_box.value()
    
class MovesDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Escolha o Número de Movimentos Aleatórios")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Escolha o número de movimentos aleatórios:")
        self.layout.addWidget(self.label)

        self.spin_box = QSpinBox()
        self.spin_box.setRange(1, 1000)
        self.spin_box.setValue(25)
        self.layout.addWidget(self.spin_box)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def get_moves(self):
        return self.spin_box.value()
    
class SolveDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Escolha o Método de Resolução")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Escolha o método de resolução:")
        self.layout.addWidget(self.label)

        self.mode_layout = QVBoxLayout()
        
        self.random_button = QPushButton("Movimentos Aleatórios")
        self.random_button.clicked.connect(lambda: self.set_mode("random"))
        self.mode_layout.addWidget(self.random_button)

        self.heuristic1_button = QPushButton("Heurística 1 - Análise em 1 Nível")
        self.heuristic1_button.clicked.connect(lambda: self.set_mode("heuristic1"))
        self.mode_layout.addWidget(self.heuristic1_button)

        self.heuristic2_button = QPushButton("Heurística 2 - Análise em 2 Níveis")
        self.heuristic2_button.clicked.connect(lambda: self.set_mode("heuristic2"))
        self.mode_layout.addWidget(self.heuristic2_button)

        self.custom_heuristic_button = QPushButton("Heurística Pessoal")
        self.custom_heuristic_button.clicked.connect(lambda: self.set_mode("custom"))
        self.mode_layout.addWidget(self.custom_heuristic_button)

        self.layout.addLayout(self.mode_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        self.selected_mode = None

    def set_mode(self, mode):
        self.selected_mode = mode

    def get_mode(self):
        return self.selected_mode   

# //MARK:- Main

def main():
    app = QApplication(sys.argv)

    size_dialog = SizeDialog()
    if size_dialog.exec() == QDialog.Accepted:
        size = size_dialog.get_size()
        initial_board = generate_goal_board(size)
        puzzle = Puzzle(initial_board)
        gui = PuzzleGUI(puzzle)
        gui.show()

        moves_dialog = MovesDialog()
        if moves_dialog.exec() == QDialog.Accepted:
            num_moves = moves_dialog.get_moves()
            gui.random_moves(num_moves)

        sys.exit(app.exec())

if __name__ == "__main__":
    main()