import requests
import os.path
import json
from lib.jsonfromfile import JsonFromFile, JsonFromFileError


class GMapsInterfaceError(Exception):
    pass


class GMapsInterface:

    def get_outcode(self, latitude, longitude):
        coords = str(latitude) + "," + str(longitude)
        params = {"latlng": coords, "result_type": "postal_code", "key": self.get_api_key()}
        response = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params)

        try:
            data = json.loads(response.text)
        except:
            raise GMapsInterfaceError("Error decoding JSON file")

        if data["status"] != "OK":
            raise GMapsInterfaceError("GMaps did not return valid response")

        try:
            address_components = data["results"][0]["address_components"]
        except KeyError:
            raise GMapsInterfaceError("GMaps did not return valid response")

        outcode = ""

        for component in address_components:
            if "postal_code" in component["types"]:
                postcode = component["long_name"]
                postcode_split = postcode.split(" ")
                outcode = postcode_split[0]

        if outcode == "":
            raise GMapsInterfaceError("No outcode found")

        return outcode

    def get_api_key(self):
        schema = {
            "type": "object",
            "gmapsApiKey": { "type": "string" },
            "required": ["gmapsApiKey"]
        }
        path = os.path.join(os.path.dirname(__file__), "../config/")
        json_data = JsonFromFile(path, schema)

        try:
            data = json_data.get_data("config")
        except JsonFromFileError:
            raise GMapsInterfaceError("No API key available")
            return

        return data["gmapsApiKey"]
