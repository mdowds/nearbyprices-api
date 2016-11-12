import json
import jsonschema
from jsonschema import validate

class JsonFromFile():

    def __init__(self, rootPath, schema):
        self.rootDataPath = rootPath
        self.schema = schema

    def getData(self, name):
        try:
            dataFile = open(self.rootDataPath + name + ".json")
        except FileNotFoundError:
            return None

        try:
            jsonData = json.loads(dataFile.read())
        except json.decoder.JSONDecodeError:
            return None

        try:
            validate(jsonData, self.schema)
        except jsonschema.exceptions.ValidationError:
            return None

        return jsonData