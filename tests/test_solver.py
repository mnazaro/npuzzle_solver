import unittest
from puzzle.board import Puzzle
from puzzle.solver import a_star

class TestSolver(unittest.TestCase):
    def test_a_star(self):
        initial_board = [
            [1, 2, 3],
            [4, 0, 5],
            [7, 8, 6]
        ]
        goal_board = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]
        puzzle = Puzzle(initial_board)
        solution = a_star(puzzle, goal_board)
        self.assertIsNotNone(solution)

if __name__ == '__main__':
    unittest.main()