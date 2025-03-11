import unittest

from unittest.mock import MagicMock
from lib.algorithms.DFS import DFS

class DFSTestCase(unittest.TestCase):
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
        self.dfs = DFS(self.start, self.goal, self.visited, self.animate, self.screen)

    # Test that initialization sets up the DFS object correctly
    def test_initialization(self):
        self.assertEqual(self.dfs.starting_cell, self.start)
        self.assertEqual(self.dfs.goal_cell, self.goal)
        self.assertEqual(self.dfs.animate, self.animate)
        self.assertEqual(self.dfs.screen, self.screen)
        self.assertFalse(self.dfs.solved)
        self.assertEqual(self.dfs.answer, [])

    # Test the get_distance method with some example inputs
    def test_get_dist(self):
        distance = self.dfs.get_distance((0, 0), (3, 4))
        
        # Add assertions to verify the correctness of the distance calculation
        self.assertEqual(distance, 7)

    # Test the get_neighbors method with some example inputs        
    def test_get_neighbors(self):
        neighbors = self.dfs.get_neighbors()
        # Assert on the expected neighbors based on the start cell and visited dictionary
        expected_neighbors = [(1, 0), (0, 1)]
        for neighbor in expected_neighbors:
            self.assertIn(neighbor, neighbors)
            
    def test_get_path(self):
        self.dfs.came_from = {(1, 0): (0, 0), (2, 0): (1, 0), (3, 0): (2, 0), (4, 0): (3, 0), (5, 0): (4, 0),
                        (5, 1): (5, 0), (5, 2): (5, 1), (5, 3): (5, 2), (5, 4): (5, 3), (5, 5): (5, 4)}
        
        self.dfs.get_path((5, 5))  # Assuming goal cell is (5, 5)
        expected_solution = [(5, 5), (5, 4), (5, 3), (5, 2), (5, 1), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0)]
        self.assertEqual(self.dfs.answer, expected_solution)
        
    def test_evaluate(self):
        self.dfs.current_cell = (0, 0)
        self.dfs.evaluation()
        self.assertNotEqual(self.dfs.state, "SOLVED")  # Assert that the state is not SOLVED yet
        
        # Test when the algorithm reaches the goal
        self.dfs.current_cell = (5, 5)  # Assuming goal cell is (5, 5)
        self.dfs.evaluation()
        print("STATE:", self.dfs.state)
        self.assertEqual(self.dfs.state, "SOLVED")  # Assert that the state changes to SOLVED
        
        # Test when the algorithm completes its execution
        # Assuming the algorithm has explored all cells and generated the answer
        self.dfs.pathdone = True
        self.dfs.solved = True
        self.dfs.evaluation()
        self.assertEqual(self.dfs.state, "DONE")  # Assert that the state changes to DONE


if __name__ == '__main__':
    unittest.main()