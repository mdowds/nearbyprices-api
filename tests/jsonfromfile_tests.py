import unittest
import json
import os.path
from lib.jsonfromfile import JsonFromFile, JsonFromFileError


class JsonFromFileTests(unittest.TestCase):

    root = os.path.dirname(__file__) + "/testdata/"

    schema = {
        "type": "object",
        "properties": {
            "areaName" : {"type" : "string"},
            "averagePrice" : {"type" : "number"}
        },
        "required": ["areaName"]
    }

    def setUp(self):
        self.jsonData = JsonFromFile(self.root, self.schema)

    def test_init_ReturnsValidObject(self):
        pricesData = JsonFromFile(self.root, self.schema)
        self.assertIsNotNone(pricesData)

    def test_init_SetsRootDataPath(self):
        self.assertEqual(self.jsonData.path, self.root)

    def test_init_SetsSchema(self):
        self.assertEqual(self.jsonData.schema, self.schema)

    def test_get_data_WithValidFilename_ReturnsCorrectData(self):
        with open(self.root + "test.json") as dataFile:
            expectedData = json.loads(dataFile.read())

        actualData = self.jsonData.get_data("test")

        self.assertEqual(actualData, expectedData)

    def test_get_data_WithInvalidFilename_Throws(self):
        self.assertRaises(JsonFromFileError, self.jsonData.get_data, "void")

    def test_get_data_WithInvalidJson_ReturnsNone(self):
        self.assertRaises(JsonFromFileError, self.jsonData.get_data, "invalid")

    def test_get_data_WithEmptyJson_ReturnsNone(self):
        self.assertRaises(JsonFromFileError, self.jsonData.get_data, "empty")

    def test_get_data_WithNoncompliantJson_ReturnsNone(self):
        self.assertRaises(JsonFromFileError, self.jsonData.get_data, "noncompliant")


if __name__ == '__main__':
    unittest.main()
