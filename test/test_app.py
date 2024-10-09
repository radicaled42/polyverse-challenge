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

if __name__ == '__main__':
    unittest.main()
