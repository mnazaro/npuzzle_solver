import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QGridLayout
from PySide6.QtWidgets import QSpinBox, QDialog, QDialogButtonBox
from PySide6.QtCore import Qt, QTimer, QRect, QPropertyAnimation
from puzzle.solver import a_star
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

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_board)
        self.layout.addWidget(self.reset_button)

        self.solve_button = QPushButton("Solve")
        self.solve_button.clicked.connect(self.solve_puzzle)
        self.layout.addWidget(self.solve_button)

        self.update_board()

    def update_board(self):
        goal_board = generate_goal_board(self.puzzle.size)
        for i in range(self.puzzle.size):
            for j in range(self.puzzle.size):
                tile = self.puzzle.board[i][j]
                # Define background color based on correct position
                color = "#90ee90" if tile != 0 and tile == goal_board[i][j] else "#ff817e"
                self.buttons[i][j].setText(str(tile) if tile != 0 else '')
                self.buttons[i][j].setStyleSheet(
                    f"font-size: 18px; background-color: {color}; color: #333;" if tile != 0 else "font-size: 18px; background-color: lightgrey;")

    def move_tile(self, i, j):
        x, y = self.puzzle.empty_tile
        if (i == x and abs(j - y) == 1) or (j == y and abs(i - x) == 1):
            direction = 'up' if i < x else 'down' if i > x else 'left' if j < y else 'right'
            self.animate_slide(i, j, direction)
            self.puzzle.move(direction)
            self.update_board()

    def animate_slide(self, i, j, direction):
        x, y = self.puzzle.empty_tile
        steps = abs(i - x) + abs(j - y)
        for step in range(steps):
            QTimer.singleShot(100*step, lambda: self.slide_tile(i, j, direction))

    def slide_tile(self, i, j, direction):
        button = self.buttons[i][j]
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(100)
        start_rect = button.geometry()
        if direction == 'up':
            end_rect = QRect(start_rect.x(), start_rect.y() - button.height(), start_rect.width(), start_rect.height())
        elif direction == 'down':
            end_rect = QRect(start_rect.x(), start_rect.y() + button.height(), start_rect.width(), start_rect.height())
        elif direction == 'left':
            end_rect = QRect(start_rect.x() - button.width(), start_rect.y(), start_rect.width(), start_rect.height())
        elif direction == 'right':
            end_rect = QRect(start_rect.x() + button.width(), start_rect.y(), start_rect.width(), start_rect.height())
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.start()

    def reset_board(self):
        self.moves_dialog = MovesDialog()
        if self.moves_dialog.exec() == QDialog.Accepted:
            num_moves = self.moves_dialog.get_moves()
            self.puzzle = Puzzle(generate_random_board(self.puzzle.size))
            self.random_moves(num_moves)
        self.update_board()

    def solve_puzzle(self):
        self.solve_dialog = SolveDialog()
        if self.solve_dialog.exec() == QDialog.Accepted:
            mode = self.solve_dialog.get_mode()
            if mode == "random":
                self.solve_steps = self.random_moves(25)
            elif mode == "heuristic1":
                self.solve_steps = a_star(self.puzzle, generate_goal_board(self.puzzle.size))
            elif mode == "heuristic2":
                self.solve_steps = a_star(self.puzzle, generate_goal_board(self.puzzle.size))
            elif mode == "custom":
                self.solve_steps = a_star(self.puzzle, generate_goal_board(self.puzzle.size))
            self.timer = QTimer()
            self.timer.timeout.connect(self.step_solution)
            self.timer.start(500)

    def step_solution(self):
        try:
            self.puzzle = next(self.solve_steps)
            self.update_board()
        except StopIteration:
            self.timer.stop()

    def random_moves(self, num_moves):
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
            self.animate_slide(*self.puzzle.empty_tile, move)
            self.puzzle.move(move)
            last_moves.append(move)
            if len(last_moves) > 2:
                last_moves.pop(0)
            self.update_board()

def generate_random_board(size):
    board = list(range(1, size*size)) + [0]
    return [board[i*size:(i+1)*size] for i in range(size)]

def generate_goal_board(size):
    return [list(range(i*size+1, (i+1)*size+1)) for i in range(size)]

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
    
def main():
    app = QApplication(sys.argv)

    size_dialog = SizeDialog()
    if size_dialog.exec() == QDialog.Accepted:
        size = size_dialog.get_size()
        initial_board = generate_random_board(size)
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