import unittest
from puzzle.utils import manhattan_distance

class TestUtils(unittest.TestCase):
    def test_manhattan_distance(self):
        board = [
            [1, 2, 3],
            [4, 0, 5],
            [7, 8, 6]
        ]
        goal = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]
        distance = manhattan_distance(board, goal)
        self.assertEqual(distance, 2)

if __name__ == '__main__':
    unittest.main()