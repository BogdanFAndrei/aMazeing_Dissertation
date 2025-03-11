import unittest

from lib.GenPoint import GenPoint
from Main import ADJWALLS, ADJACENTS, OPWALLS

class GenpointTestCase(unittest.TestCase):
    def setUp(self):
        # Set up any common test data or mocks needed for the tests
    # Is run before each test to set up a clean slate for test case
        self.border = [(0, 1), (1, 0)]  # Sample border
        self.gencell = ((0, 0), 0b0000)  # Sample generation cell
        self.gen_point = GenPoint(self.gencell, self.border)

    # Add assertions to check if the initialization is done correctly
    def test_initialization(self):
        # Set gencell after bounds are determined
        self.gencell = ((0, 0), 0b1001)
        # Test assertions
        self.assertEqual(self.gen_point.gencell, self.gencell)
        self.assertIsNone(self.gen_point.gen_id)
        self.assertEqual(self.gen_point.genbound, 0b1001)
        self.assertEqual(self.gen_point.current_cell, [])
        self.assertEqual(self.gen_point.visited, {})
        self.assertEqual(self.gen_point.border, self.border)
        self.assertEqual(self.gen_point.stack, [[], [], [], []])
    
    def test_get_neighbors(self):
        neighbors = self.gen_point.get_neighbors((1, 1))  # Test with a known cell
        expected_neighbors = [((2, 1), 1), ((1, 2), 8)]  # Expected neighbors
        self.assertEqual(neighbors, expected_neighbors)

    def test_get_gen_bounds(self):
        self.gen_point.get_gen_bounds()
        expected_genbound = 0b1001  # Example expected genbound
        self.assertEqual(self.gen_point.genbound, expected_genbound)
        
if __name__ == '__main__':
    unittest.main()