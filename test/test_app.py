import unittest
from main import app
from unittest.mock import patch

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('map_handler.MapHandler.show_local_polyverse')
    def test_show_local(self, mock_show):
        mock_show.return_value = [["P", "S", "C"]]
        response = self.app.get('/show')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Element written successfully!', response.data)

    @patch('map_handler.MapHandler.merge_map')
    @patch('map_handler.MapHandler.write_local_map')
    def test_write_map(self, mock_write, mock_merge):
        mock_merge.return_value = [1]
        mock_write.return_value = 1
        data = {
            "start": "(1,1)",
            "payload": {"type": 2, "direction": "up"}
        }
        response = self.app.post('/write', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Writing action completed successfully!', response.data)

    @patch('map_handler.MapHandler.clean_polyverse')
    def test_clean_polyverse(self, mock_clean):
        response = self.app.post('/clean')
        mock_clean.assert_called_once()
        self.assertEqual(response.status_code, 200)

    @patch('map_handler.MapHandler.duplicate_polyverse')
    def test_duplicate_map(self, mock_duplicate):
        mock_duplicate.return_value = [1]
        data = {
            "url": "https://someurl.com"
        }
        response = self.app.post('/duplicate', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Duplication action completed successfully!', response.data)


if __name__ == '__main__':
    unittest.main()
