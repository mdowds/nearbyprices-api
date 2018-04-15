import os.path
from lib.jsonfromfile import JsonFromFile, JsonFromFileError


class PricesFromOutcode:

    schema = {
        "type": "object",
        "properties": {
            "areaName": {"type": "string"},
            "averagePrice": {"type": "number"},
            "detachedAverage": {"type": "number"},
            "flatAverage": {"type": "number"},
            "outcode": {"type": "string"},
            "semiDetachedAverage": {"type": "number"},
            "terracedAverage": {"type": "number"},
            "transactionCount": {"type": "number"}
        },
        "required": ["areaName", "averagePrice", "outcode", "transactionCount"]
    }

    data_path = os.path.join(os.path.dirname(__file__), "../data/")

    def get_prices(self, outcode):
        json_data = JsonFromFile(self.data_path, self.schema)

        try:
            data = json_data.get_data(outcode.lower())
        except JsonFromFileError as err:
            raise err

        return data
