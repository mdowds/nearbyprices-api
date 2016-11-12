import unittest
import json
import os
from jsonfromfile import JsonFromFile


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
        self.assertEqual(self.jsonData.rootDataPath, self.root)

    def test_init_SetsSchema(self):
        self.assertEqual(self.jsonData.schema, self.schema)

    def test_getData_WithValidFilename_ReturnsCorrectData(self):
        dataFile = open(self.root + "test.json").read()
        expectedData = json.loads(dataFile)

        actualData = self.jsonData.getData("test")

        self.assertEqual(actualData, expectedData)

    def test_getData_WithInvalidFilename_ReturnsNone(self):
        self.assertIsNone(self.jsonData.getData("void"))

    def test_getData_WithInvalidJson_ReturnsNone(self):
        self.assertIsNone(self.jsonData.getData("invalid"))

    def test_getData_WithEmptyJson_ReturnsNone(self):
        self.assertIsNone(self.jsonData.getData("empty"))

    def test_getData_WithNoncompliantJson_ReturnsNone(self):
        self.assertIsNone(self.jsonData.getData("noncompliant"))


if __name__ == '__main__':
    unittest.main()
