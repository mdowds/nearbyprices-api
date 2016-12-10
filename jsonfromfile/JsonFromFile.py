import json
import os.path
import jsonschema
from jsonschema import validate


class JsonFromFileError(Exception):
    pass


class JsonFromFile():

    def __init__(self, root_path, schema):
        self.data_path = os.path.join(os.path.dirname(__file__), '..', root_path)
        self.schema = schema

    def get_data(self, name):
        try:
            data_file = open(self.data_path + name + ".json")
        except FileNotFoundError:
            raise JsonFromFileError("File not found")

        try:
            json_data = json.loads(data_file.read())
        except json.decoder.JSONDecodeError:
            raise JsonFromFileError("Error decoding JSON file")

        try:
            validate(json_data, self.schema)
        except jsonschema.exceptions.ValidationError:
            raise JsonFromFileError("Error validating JSON file")

        return json_data
