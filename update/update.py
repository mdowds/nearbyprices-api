import os.path
import json
from datasource import PricesDataSource, PricesDataSourceError


def update_price_data():
    path = os.path.dirname(__file__)
    outcodes_file = open(path + 'outcodes.json')
    outcodes_array = json.load(outcodes_file)

    record_count = 0

    for outcode in outcodes_array:
        print("Fetching data for " + outcode)
        datasource = PricesDataSource(outcode)
        datasource.run_query()

        try:
            results = datasource.get_results_dictionary()
            with open(path + 'data/' + outcode.lower() + '.json', 'w') as output_file:
                json.dump(results, output_file, sort_keys=True)
                print("File " + output_file.name + " created and written to")
                record_count += 1

        except PricesDataSourceError as error:
            print("An error occurred: " + str(error))

    outcodes_file.close()
    print(str(record_count) + " records created")


if __name__ == '__main__':
    update_price_data()
