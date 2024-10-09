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

if __name__ == '__main__':
    unittest.main()
