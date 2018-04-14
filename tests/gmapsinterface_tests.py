import unittest
from unittest.mock import patch
import os.path
from lib.gmapsinterface import GMapsInterface, GMapsInterfaceError


class GMapsInterfaceTests(unittest.TestCase):

    example_lat = 51.507386
    example_long = -0.127651
    mock_key = "1234"

    path = os.path.dirname(__file__)

    def setUp(self):
        os.environ["GMAPS_API_KEY"] = self.mock_key
        self.maps = GMapsInterface()

    @patch('lib.gmapsinterface.requests')
    def test_init_makesRequestToMapsAPI(self, mock_requests):
        mock_requests.get.return_value.text = self.get_sample_response("gmapssample")
        self.maps.get_outcode(self.example_lat, self.example_long)

        coords_str = str(self.example_lat) + "," + str(self.example_long)
        expected_params = {"latlng": coords_str, "result_type": "postal_code", "key": self.mock_key}

        mock_requests.get.assert_called_once_with("https://maps.googleapis.com/maps/api/geocode/json", expected_params)

    @patch('lib.gmapsinterface.requests')
    def test_init_returnsOutcode(self, mock_requests):
        mock_requests.get.return_value.text = self.get_sample_response("gmapssample")
        actual = self.maps.get_outcode(self.example_lat, self.example_long)

        self.assertEqual(actual, "WC2N")

    @patch('lib.gmapsinterface.requests')
    def test_init_withNilGMapsResponse_Raises(self, mock_requests):
        mock_requests.get.return_value.text = None
        self.assertRaises(GMapsInterfaceError, self.maps.get_outcode, self.example_lat, self.example_long)

    @patch('lib.gmapsinterface.requests')
    def test_init_withGMapsResponseError_Raises(self, mock_requests):
        mock_requests.get.return_value.text = self.get_sample_response("gmapserror")
        self.assertRaises(GMapsInterfaceError, self.maps.get_outcode, self.example_lat, self.example_long)

    @patch('lib.gmapsinterface.requests')
    def test_init_withEmptyGmapsResponse_Raises(self, mock_requests):
        mock_requests.get.return_value.text = self.get_sample_response("gmapsempty")
        self.assertRaises(GMapsInterfaceError, self.maps.get_outcode, self.example_lat, self.example_long)

    # Helper functions

    def get_sample_response(self, name):
        path = os.path.join(self.path, "testdata/")
        with open(path + name + ".json") as file:
            return file.read()


if __name__ == '__main__':
    unittest.main()
