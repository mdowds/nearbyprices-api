from flask import Flask
from flask_restful import Resource, Api, abort
from webargs import fields, ValidationError
from webargs.flaskparser import use_kwargs, parser
from lib.gmapsinterface import GMapsInterface, GMapsInterfaceError
from lib.pricesfromoutcode import PricesFromOutcode

app = Flask(__name__)
api = Api(app)

MAXIMUM_LATITUDE = 60.86
MINIMUM_LATITUDE = 49.86
MAXIMUM_LONGITUDE = 1.78
MINIMUM_LONGITUDE = -8.45


class outcode(Resource):

    def get(self, outcode):
        pfo = PricesFromOutcode()

        try:
            data = pfo.get_prices(outcode)
        except Exception as err:
            abort(400, errors=str(err))
            return

        return data


class position(Resource):

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
        maps = GMapsInterface()

        try:
            outcode = maps.get_outcode(lat, long)
        except GMapsInterfaceError as err:
            abort(400, errors=str(err))
            return

        pfo = PricesFromOutcode()

        try:
            data = pfo.get_prices(outcode)
        except Exception as err:
            abort(400, errors=str(err))
            return

        return data

api.add_resource(outcode, '/prices/outcode/<string:outcode>')
api.add_resource(position, '/prices/position')


@parser.error_handler
def handle_request_parsing_error(err):
    abort(400, errors=err.messages)

if __name__ == '__main__':
     app.run()
