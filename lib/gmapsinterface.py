import requests
import os
import json


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
        return os.environ.get('GMAPS_API_KEY')
