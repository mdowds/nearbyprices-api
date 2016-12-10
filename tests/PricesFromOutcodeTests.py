import unittest
from unittest.mock import patch
from api import PricesFromOutcode
from jsonfromfile import JsonFromFileError


class PricesFromPositionTests(unittest.TestCase):

    def setUp(self):
        self.pfp = PricesFromOutcode()

    @patch('api.JsonFromFile')
    def test_get_callsJFFinit_withDefaultDirAndSchema(self, mock_JsonFromFile):
        self.pfp.get("e17")
        args = mock_JsonFromFile.call_args

        self.assertTrue(type(args[0][0]) == str, "First parameter of JsonFromFile init was not a string")
        self.assertTrue(type(args[0][1]) == dict, "Second parameter of JsonFromFile init was not a dictionary")

    @patch('api.JsonFromFile')
    def test_get_callsJFFGetData_withOutcode(self, mock_JsonFromFile):
        self.pfp.get("e17")
        mock_JsonFromFile.return_value.get_data.assert_called_once_with("e17")

    @patch('api.JsonFromFile')
    def test_get_withUpperOutcode_callsJFFGetData_withOutcode(self, mock_JsonFromFile):
        self.pfp.get("E17")
        mock_JsonFromFile.return_value.get_data.assert_called_once_with("e17")

    @patch('api.JsonFromFile')
    def test_get_ReturnsDataReturnedFromJFF(self, mock_JsonFromFile):
        data = { "sample" }
        mock_JsonFromFile.return_value.get_data.return_value = data
        self.assertEqual(self.pfp.get("e17"), data)

    @patch('api.abort')
    @patch('api.JsonFromFile')
    def test_get_whenReturnedError_CallsAbort(self, mock_JsonFromFile, mock_abort):
        err = JsonFromFileError()
        mock_JsonFromFile.return_value.get_data.side_effect = err
        self.pfp.get("e17")
        mock_abort.assert_called_once_with(400, errors=str(err))


if __name__ == '__main__':
    unittest.main()
