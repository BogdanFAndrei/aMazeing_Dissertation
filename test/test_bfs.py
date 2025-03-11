import queue
import unittest

from unittest.mock import MagicMock
from lib.algorithms.BFS import BFS


class BFSTestCase(unittest.TestCase):
    # Set up any common test data or mocks needed for the tests
    # Is run before each test to set up a clean slate for test case
    def setUp(self):
        # Set up mock data or objects for testing
        self.start = (0, 0)
        self.goal = (5, 5)
        self.visited = {
            (0, 0): 0b1111,
            (1, 0): 0b1100,
            (0, 1): 0b1010, 
        }  # Sample visited dictionary
        self.animate = False
        self.screen = MagicMock()  # Mock screen object
        self.bfs = BFS(self.start, self.goal, self.visited, self.animate, self.screen)

    # Add assertions to check if the initialization is done correctly
    def test_initialization(self):
        self.assertEqual(self.bfs.starting_cell, self.start)
        self.assertEqual(self.bfs.goal_cell, self.goal)
        self.assertEqual(self.bfs.animate, self.animate)
        self.assertEqual(self.bfs.screen, self.screen)        
        self.assertFalse(self.bfs.solved)
        self.assertEqual(self.bfs.answer, [])

    # Test the get_distance method with some example inputs
    def test_get_dist(self):
        distance = self.bfs.get_distance((0, 0), (3, 4))
        
        # Add assertions to verify the correctness of the distance calculation
        self.assertEqual(distance, 7)

    def test_get_neighbors(self):
        self.bfs.current_cell = (0, 0)
        
        neighbors = self.bfs.get_neighbors()
        # Add assertions to verify the correctness of the returned neighbors
        expected_neighbors = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.assertEqual(neighbors, expected_neighbors)

    def test_get_path(self):
        # Call the get_path method with a mocked cell
        self.bfs.came_from = {(1, 0): (0, 0), (2, 0): (1, 0), (3, 0): (2, 0), (4, 0): (3, 0), (5, 0): (4, 0),
                        (5, 1): (5, 0), (5, 2): (5, 1), (5, 3): (5, 2), (5, 4): (5, 3), (5, 5): (5, 4)}
        
        self.bfs.get_path((5, 5))  # Assuming goal cell is (5, 5)
        expected_solution = [(5, 5), (5, 4), (5, 3), (5, 2), (5, 1), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0)]
        # Assert that the answer is correctly populated
        self.assertEqual(self.bfs.answer, expected_solution)

    def test_evaluate(self):
        self.bfs.openset.put((1, 0))
        self.bfs.openset.put((0, 1))
        self.bfs.current_cell = (0, 0)
        self.bfs.evaluation()
        print("STATE:", self.bfs.state)
        self.assertNotEqual(self.bfs.state, "SOLVED")  # Assert that the state is not SOLVED yet
        
        # Test when the algorithm reaches the goal
        # Clear openset and set the current cell to the goal cell
        self.bfs.openset = queue.Queue()
        self.bfs.openset.put((5, 5))
        self.bfs.current_cell = (5, 5)  # Assuming goal cell is (5, 5)
        self.bfs.evaluation()
        print("STATE:", self.bfs.state)
        self.assertEqual(self.bfs.state, "SOLVED")  # Assert that the state changes to SOLVED
        
        # Test when the algorithm completes its execution
        # Assuming the algorithm has explored all cells and generated the answer
        self.bfs.pathdone = True
        self.bfs.solved = True
        self.bfs.evaluation()
        print("STATE:", self.bfs.state)
        self.assertEqual(self.bfs.state, "DONE")  # Assert that the state changes to DONE

if __name__ == '__main__':
    unittest.main()