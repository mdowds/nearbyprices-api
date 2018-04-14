import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError


class JsonFromFileError(Exception):
    pass


class JsonFromFile:

    def __init__(self, path, schema):
        self.path = path
        self.schema = schema

    def get_data(self, name):
        try:
            with open(self.path + name + ".json") as data_file:
                try:
                    json_data = json.loads(data_file.read())
                except json.decoder.JSONDecodeError as err:
                    raise JsonFromFileError("Error decoding JSON file") from err

                try:
                    validate(json_data, self.schema)
                except ValidationError as err:
                    raise JsonFromFileError("Error validating JSON file") from err

                return json_data

        except FileNotFoundError as err:
            raise JsonFromFileError("File not found") from err
