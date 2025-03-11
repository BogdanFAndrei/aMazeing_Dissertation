import unittest

from unittest.mock import MagicMock
from lib.CellDraw import _CellDraw

class CellDrawTestCase(unittest.TestCase):
    
    def setUp(self):
        # Mocking screen object
        self.mock_screen = MagicMock()
        
        # Mocking _CellDraw object
        self.cell_draw = _CellDraw()
        self.cell_draw.screen = self.mock_screen
        self.cell_draw.cell_size = (10, 10)  # Example values for cell_size, wall_size, and buffer_settings
        self.cell_draw.wall_size = (2, 2)
        self.cell_draw.buffer_settings = (1, 1)
        self.cell_draw.core_size = (6, 6)
    
    def test_draw_core(self):
        # Test draw_core method
        cell = ((1, 2), 0b0000)  # Example cell
        color = (255, 255, 255)  # Example color
        self.cell_draw.draw_core(cell, color)
        expected_result = (1*10+2+1, 2*10+2+1), (6, 6)
        self.mock_screen.fill.assert_called_once_with(color, expected_result)
        
    def test_draw_walls(self):
        # Test draw_walls method
        cell = ((1, 2), 0b1100)  # Example cell with top and right walls
        color = (255, 255, 255)  # Example color
        self.cell_draw.draw_walls(cell, color)
        expected_calls = [((255, 255, 255), ((1*10+2+1, 2*10+1), (6, 2)),), ((255, 255, 255), ((1*10+10+1, 2*10+2+1), (2, 6)))]
        actual_calls = [call[0] for call in self.mock_screen.fill.call_args_list]
        self.assertEqual(actual_calls, expected_calls)

if __name__ == '__main__':
    unittest.main()
