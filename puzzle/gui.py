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
        self.setWindowTitle("8 Puzzle Game")
        self.setGeometry(100, 100, 400, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        self.title = QLabel("8 Puzzle Game")
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
        for i in range(self.puzzle.size):
            for j in range(self.puzzle.size):
                tile = self.puzzle.board[i][j]
                self.buttons[i][j].setText(str(tile) if tile != 0 else '')
                self.buttons[i][j].setStyleSheet(
                    "font-size: 18px; background-color: #f8f8f8; color: #333;" if tile != 0 else "font-size: 18px; background-color: lightgrey;")

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
        self.puzzle = Puzzle(generate_random_board(self.puzzle.size))
        self.update_board()

    def solve_puzzle(self):
        goal_board = generate_goal_board(self.puzzle.size)
        solution = a_star(self.puzzle, goal_board)
        if solution:
            for step in solution:
                self.puzzle = step
                self.update_board()
                QTimer.singleShot(500, lambda: None)  # Delay para visualizar os passos

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
        self.spin_box.setRange(1, 100)
        self.spin_box.setValue(10)
        self.layout.addWidget(self.spin_box)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def get_moves(self):
        return self.spin_box.value()
    
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