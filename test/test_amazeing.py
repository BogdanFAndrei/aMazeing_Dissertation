import unittest

from unittest.mock import MagicMock
from lib.amazeing import AMazeing


class AmazeingTestCase(unittest.TestCase):
    def setUp(self):
        # Set up mock data or objects for testing
        pass

    def test_init(self):
        self.maze = AMazeing('DFS')
        self.assertEqual(self.maze.state, "START")
        self.assertTrue(self.maze.animate)