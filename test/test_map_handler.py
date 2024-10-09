import unittest
from unittest.mock import patch
from polyverse.api import PolyverseAPI
from polyverse.map_handler import MapHandler

class MapHandlerTestCase(unittest.TestCase):

    @patch('api.PolyverseAPI.get_polyverse_map')
    def setUp(self, mock_get_map):
        # Mock the API response
        mock_get_map.return_value = [
            [{'type': 0}, None, {'type': 1}],
            [None, {'type': 2}, None]
        ]
        # Create API and MapHandler instances
        self.api = PolyverseAPI("https://fakeurl.com", "candidate-id")
        self.map_handler = MapHandler(self.api)

    def test_show_local_polyverse(self):
        result = self.map_handler.show_local_polyverse()
        expected_result = [['P', '-', 'S'], ['-', 'C', '-']]
        self.assertEqual(result, expected_result)

    @patch('api.PolyverseAPI.write_element')
    def test_write_local_map(self, mock_write):
        element_data = {"row": 0, "column": 1, "payload": {"type": 1, "color": "blue"}}
        self.map_handler.write_local_map(element_data)
        mock_write.assert_called_once()

    @patch('api.PolyverseAPI.delete_element')
    def test_delete_local_map(self, mock_delete):
        element_data = {"row": 1, "column": 2, "payload": {"type": 1}}
        self.map_handler.delete_local_map(element_data)
        mock_delete.assert_called_once()


if __name__ == '__main__':
    unittest.main()
