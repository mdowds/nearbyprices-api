from flask import Flask, jsonify
from flask_restful import Resource, Api
from jsonfromfile import JsonFromFile

app = Flask(__name__)
api = Api(app)

class Hello(Resource):
    def get(self):
        return("Hello world")

class Prices(Resource):

    schema = {
        "type": "object",
        "properties": {
            "areaName": {"type": "string"},
            "averagePrice": {"type": "number"},
            "detachedAverage": {"type": "number"},
            "flatAverage": {"type": "number"},
            "outcode": {"type": "string"},
            "pastAveragePrice": {"type": "number"},
            "priceChange": {"type": "number"},
            "semiDetachedAverage": {"type": "number"},
            "terracedAverage": {"type": "number"},
            "transactionCount": {"type": "number"}
        },
        "required": ["areaName","averagePrice","outcode","transactionCount"]
    }

    def get(self, outcode):
        jsonData = JsonFromFile("data/", self.schema)

        data = jsonData.getData(outcode.lower())

        if(data == None):
            return jsonify({ "error": "An error occured: no valid data returned"})

        return jsonify(data)

api.add_resource(Hello, '/')
api.add_resource(Prices, '/prices/<string:outcode>')

if __name__ == '__main__':
     app.run(debug=True)