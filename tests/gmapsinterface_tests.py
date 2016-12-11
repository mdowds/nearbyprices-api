import unittest
from unittest.mock import patch
import json
import os.path
from lib.gmapsinterface import GMapsInterface, GMapsInterfaceError


class GMapsInterfaceTests(unittest.TestCase):

    example_lat = 51.507386
    example_long = -0.127651

    path = os.path.dirname(__file__)

    def setUp(self):
        self.maps = GMapsInterface()

    @patch('lib.gmapsinterface.requests')
    def test_init_makesRequestToMapsAPI(self, mock_requests):
        mock_requests.get.return_value = self.get_sample_response("gmapssample")
        self.maps.get_outcode(self.example_lat, self.example_long)

        coords_str = str(self.example_lat) + "," + str(self.example_long)
        expected_params = { "latlng": coords_str, "result_type": "postal_code", "key": self.get_api_key()}

        mock_requests.get.assert_called_once_with("https://maps.googleapis.com/maps/api/geocode/json", expected_params)

    @patch('lib.gmapsinterface.requests')
    def test_init_returnsOutcode(self, mock_requests):
        mock_requests.get.return_value = self.get_sample_response("gmapssample")
        actual = self.maps.get_outcode(self.example_lat, self.example_long)

        self.assertEqual(actual, "WC2N")

    @patch('lib.gmapsinterface.requests')
    def test_init_withNilGMapsResponse_Raises(self, mock_requests):
        mock_requests.get.return_value = None
        self.assertRaises(GMapsInterfaceError, self.maps.get_outcode, self.example_lat, self.example_long)

    @patch('lib.gmapsinterface.requests')
    def test_init_withGMapsResponseError_Raises(self, mock_requests):
        mock_requests.get.return_value = self.get_sample_response("gmapserror")
        self.assertRaises(GMapsInterfaceError, self.maps.get_outcode, self.example_lat, self.example_long)

    @patch('lib.gmapsinterface.requests')
    def test_init_withEmptyGmapsResponse_Raises(self, mock_requests):
        mock_requests.get.return_value = self.get_sample_response("gmapsempty")
        self.assertRaises(GMapsInterfaceError, self.maps.get_outcode, self.example_lat, self.example_long)

    # Helper functions

    def get_sample_response(self, name):
        path = os.path.join(self.path, "testdata/")
        file = open(path + name + ".json")
        return file.read()

    def get_api_key(self):
        path = os.path.join(self.path, "../config/")
        file = open(path + "config.json")
        data = json.loads(file.read())
        return data['gmapsApiKey']


if __name__ == '__main__':
    unittest.main()
