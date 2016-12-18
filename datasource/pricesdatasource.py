from datasource.landregistryinterface import LandRegistryInterface
from datasource.landregistryqueryfactory import LandRegistryQueryFactory


class PricesDataSource:
    error = ""

    # Constants
    CURRENT_YEAR_MAX = 1
    CURRENT_YEAR_MIN = 0
    PAST_YEAR_MAX = 2
    PAST_YEAR_MIN = 1

    TYPE_KEY = 'type'
    PROPERTYTYPE_KEY = 'ppd_propertyType'
    ERROR_KEY = 'error'
    RESULTS_KEY = 'results'
    BINDINGS_KEY = 'bindings'
    TOWN_KEY = 'town'
    VALUE_KEY = 'value'

    # These are the properties of the returned object
    OUTCODE_KEY = 'outcode'
    AREANAME_KEY = 'areaName'
    AVERAGEPRICE_KEY = 'averagePrice'
    TRANSACTIONCOUNT_KEY = 'transactionCount'
    PASTAVERAGEPRICE_KEY = 'pastAveragePrice'
    PRICECHANGE_KEY = 'priceChange'
    DETACHEDAVERAGE_KEY = 'detachedAverage'
    SEMIAVERAGE_KEY = 'semiDetachedAverage'
    TERRACEDAVERAGE_KEY = 'terracedAverage'
    FLATAVERAGE_KEY = 'flatAverage'

    def __init__(self, outcode):
        self.outcode = outcode.upper()

    def run_query(self):
        # Main query
        main_query = LandRegistryQueryFactory.main_query(self.outcode)
        self.main_query_results = LandRegistryInterface.run_query(main_query)

        # Property type query
        type_query = LandRegistryQueryFactory.type_query(self.outcode)
        self.type_query_results = LandRegistryInterface.run_query(type_query)

        # Value change query
        change_query = LandRegistryQueryFactory.change_query(self.outcode)
        self.change_query_results = LandRegistryInterface.run_query(change_query)

        self.process_results()

    # Return results

    def get_results_dictionary(self):
        if self.error == "":
            return {
                self.OUTCODE_KEY: self.outcode,
                self.AREANAME_KEY: self.area_name,
                self.AVERAGEPRICE_KEY: self.average_price,
                self.TRANSACTIONCOUNT_KEY: self.transaction_count,
                self.PASTAVERAGEPRICE_KEY: self.past_average_price,
                self.PRICECHANGE_KEY: self.price_change,
                self.DETACHEDAVERAGE_KEY: self.detached_average,
                self.SEMIAVERAGE_KEY: self.semi_detached_average,
                self.TERRACEDAVERAGE_KEY: self.terraced_average,
                self.FLATAVERAGE_KEY: self.flat_average
            }
        else:
            return {'error': self.error}

    # Helper methods

    def process_results(self):
        if 'error' in self.main_query_results or 'error' in self.type_query_results:
            self.error = self.main_query_results['error']
            return

        results = self.main_query_results[self.RESULTS_KEY][self.BINDINGS_KEY][0]
        typeResults = self.type_query_results[self.RESULTS_KEY][self.BINDINGS_KEY]
        changeResults = self.change_query_results[self.RESULTS_KEY][self.BINDINGS_KEY][0]

        if self.TOWN_KEY in results:
            self.area_name = results[self.TOWN_KEY][self.VALUE_KEY].title()
            self.average_price = int(float(results[self.AVERAGEPRICE_KEY][self.VALUE_KEY]))
            self.transaction_count = int(results[self.TRANSACTIONCOUNT_KEY][self.VALUE_KEY])

            self.past_average_price = int(float(changeResults[self.AVERAGEPRICE_KEY][self.VALUE_KEY]))
            self.price_change = ((self.average_price / self.past_average_price) - 1) * 100

            for binding in typeResults:

                if self.check_type(binding, "detached"):
                    self.detached_average = int(float(binding[self.AVERAGEPRICE_KEY][self.VALUE_KEY]))
                elif self.check_type(binding, "semi-detached"):
                    self.semi_detached_average = int(float(binding[self.AVERAGEPRICE_KEY][self.VALUE_KEY]))
                elif self.check_type(binding, "terraced"):
                    self.terraced_average = int(float(binding[self.AVERAGEPRICE_KEY][self.VALUE_KEY]))
                elif self.check_type(binding, "flat-maisonette"):
                    self.flat_average = int(float(binding[self.AVERAGEPRICE_KEY][self.VALUE_KEY]))

        else:
            self.error = "Malformed outcode"
            return

    def check_type(self, binding, propertyType):
        typeDefUrl = "http://landregistry.data.gov.uk/def/common/"

        if (self.PROPERTYTYPE_KEY in binding and
                binding[self.PROPERTYTYPE_KEY][self.VALUE_KEY] == typeDefUrl + propertyType
                and int(binding['transactionCount'][self.VALUE_KEY]) > 0):
            return True
        else:
            return False

    def check_errors(self, results):
        if 'error' in results:
            self.error = self.main_query_results['error']
            return True

        if int(results[self.RESULTS_KEY][self.BINDINGS_KEY][0][self.TRANSACTIONCOUNT_KEY][self.VALUE_KEY]) == 0:
            self.error = "No results found"
            return True

        if self.TOWN_KEY not in results[self.RESULTS_KEY][self.BINDINGS_KEY][0]:
            self.error = "Malformed outcode"
            return True

        return False