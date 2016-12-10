import json
import os.path
import jsonschema
from jsonschema import validate


class JsonFromFile():

    def __init__(self, rootPath, schema):
        self.rootDataPath = os.path.join(os.path.dirname(__file__), '..', rootPath)
        self.schema = schema

    def getData(self, name):
        try:
            dataFile = open(self.rootDataPath + name + ".json")
        except FileNotFoundError:
            print("FileNotFoundError")
            return None

        try:
            jsonData = json.loads(dataFile.read())
        except json.decoder.JSONDecodeError:
            print("JSONDecodeError")
            return None

        try:
            validate(jsonData, self.schema)
        except jsonschema.exceptions.ValidationError:
            print("ValidationError")
            return None

        return jsonData
