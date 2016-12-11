import unittest
from unittest.mock import patch
from lib.pricesfromoutcode import PricesFromOutcode
from lib.jsonfromfile import JsonFromFileError


class PricesFromOutcodeTests(unittest.TestCase):

    def setUp(self):
        self.pfo = PricesFromOutcode()

    @patch('lib.pricesfromoutcode.JsonFromFile')
    def test_get_callsJFFinit_withDefaultDirAndSchema(self, mock_JsonFromFile):
        self.pfo.get_prices("e17")
        args = mock_JsonFromFile.call_args

        self.assertTrue(type(args[0][0]) == str, "First parameter of JsonFromFile init was not a string")
        self.assertTrue(type(args[0][1]) == dict, "Second parameter of JsonFromFile init was not a dictionary")

    @patch('lib.pricesfromoutcode.JsonFromFile')
    def test_get_callsJFFGetData_withOutcode(self, mock_JsonFromFile):
        self.pfo.get_prices("e17")
        mock_JsonFromFile.return_value.get_data.assert_called_once_with("e17")

    @patch('lib.pricesfromoutcode.JsonFromFile')
    def test_get_withUpperOutcode_callsJFFGetData_withOutcode(self, mock_JsonFromFile):
        self.pfo.get_prices("E17")
        mock_JsonFromFile.return_value.get_data.assert_called_once_with("e17")

    @patch('lib.pricesfromoutcode.JsonFromFile')
    def test_get_ReturnsDataReturnedFromJFF(self, mock_JsonFromFile):
        data = { "sample" }
        mock_JsonFromFile.return_value.get_data.return_value = data
        self.assertEqual(self.pfo.get_prices("e17"), data)

    @patch('lib.pricesfromoutcode.JsonFromFile')
    def test_get_whenReturnedError_Raises(self, mock_JsonFromFile):
        err = JsonFromFileError()
        mock_JsonFromFile.return_value.get_data.side_effect = err
        self.assertRaises(JsonFromFileError, self.pfo.get_prices, "e17")


if __name__ == '__main__':
    unittest.main()
