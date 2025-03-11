import unittest

from unittest.mock import MagicMock, patch
from lib.algorithms.Astar import Solver

class AstarTestCase(unittest.TestCase):
    
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
        self.screen = MagicMock()
        self.solver = Solver(self.start,self.goal,self.visited,self.animate,self.screen)
        
    # Test that initialization sets up the DFS object correctly
    def test_initialization(self):
        self.assertEqual(self.solver.starting_cell, self.start)
        self.assertEqual(self.solver.goal_cell, self.goal)
        self.assertEqual(self.solver.animate, self.animate)
        self.assertEqual(self.solver.screen, self.screen)
        self.assertFalse(self.solver.solved)
        self.assertEqual(self.solver.answer, [])
        self.assertIsNotNone(self.solver)

    def test_get_dist(self):
        dist = self.solver.get_distance((0, 0), (3, 4))
        self.assertEqual(dist, 7)

    def test_get_neighbors(self):
        neighbors = self.solver.get_neighbors()
        expected_neighbors = {(1, 0), (0, 1), (-1, 0), (0, -1)}
        self.assertEqual(neighbors, expected_neighbors)

    def test_get_openset(self):
        self.solver.current_cell = (0, 0)
        self.solver.get_openset()
        expected_openset = {(1, 0), (0, 1), (-1, 0), (0, -1)} 
        self.assertEqual(self.solver.openset, expected_openset)

    def test_get_path(self):
        self.solver.came_from = {(1, 0): (0, 0), (2, 0): (1, 0), (3, 0): (2, 0), (4, 0): (3, 0), (5, 0): (4, 0),
                        (5, 1): (5, 0), (5, 2): (5, 1), (5, 3): (5, 2), (5, 4): (5, 3), (5, 5): (5, 4)}
        self.solver.current_cell = (5, 5)
        self.solver.get_path((5, 5))
        expected_solwalls = {(5, 5): 8}
        self.assertEqual(self.solver.solwalls, expected_solwalls)


    def test_evaluate(self):
        self.solver.openset = {(1, 0), (0, 1)}
        self.solver.current_cell = (0, 0)
        self.solver.evaluation()
        expected_closedset = {(1, 0), (0,0)}
        self.assertEqual(self.solver.close_setting, expected_closedset)

if __name__ == '__main__':
    unittest.main()
