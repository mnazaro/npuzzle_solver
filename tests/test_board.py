import unittest
from puzzle.board import Puzzle

class TestPuzzle(unittest.TestCase):
    def test_move(self):
        initial_board = [
            [1, 2, 3],
            [4, 0, 5],
            [7, 8, 6]
        ]
        puzzle = Puzzle(initial_board)
        puzzle.move('down')
        self.assertEqual(puzzle.board, [
            [1, 2, 3],
            [4, 8, 5],
            [7, 0, 6]
        ])

if __name__ == '__main__':
    unittest.main()