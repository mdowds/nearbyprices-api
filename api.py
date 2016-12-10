from flask import Flask
from flask_restful import Resource, Api, abort
from jsonfromfile import JsonFromFile, JsonFromFileError
from webargs import fields, ValidationError
from webargs.flaskparser import use_kwargs, parser

app = Flask(__name__)
api = Api(app)

MAXIMUM_LATITUDE = 60.86
MINIMUM_LATITUDE = 49.86
MAXIMUM_LONGITUDE = 1.78
MINIMUM_LONGITUDE = -8.45


class PricesFromOutcode(Resource):

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

    defaultdir = "data/"

    def get(self, outcode):
        json_data = JsonFromFile(self.defaultdir, self.schema)

        try:
            data = json_data.get_data(outcode.lower())
        except JsonFromFileError as err:
            abort(400, errors=str(err))
            return

        return data


class PricesFromPosition(Resource):

    def validate_latitude(val):
        if not MAXIMUM_LATITUDE >= val >= MINIMUM_LATITUDE:
            raise ValidationError('Invalid latitude')

    def validate_longitude(val):
        if not MAXIMUM_LONGITUDE >= val >= MINIMUM_LONGITUDE:
            raise ValidationError('Invalid latitude')

    args = {
        'lat': fields.Float(
            required=True,
            validate=validate_latitude
        ),
        'long': fields.Float(
            required=True,
            validate=validate_longitude
        )
    }

    @use_kwargs(args)
    def get(self, lat, long):
        return {'lat': lat, 'long': long}

api.add_resource(PricesFromOutcode, '/prices/outcode/<string:outcode>')
api.add_resource(PricesFromPosition, '/prices/position')


@parser.error_handler
def handle_request_parsing_error(err):
    abort(400, errors=err.messages)

if __name__ == '__main__':
     app.run(debug=True)
