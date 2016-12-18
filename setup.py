import os.path
import json
from datasource.pricesdatasource import PricesDataSource, PricesDataSourceError

path = os.path.dirname(__file__)
outcodes_file = open(path + '/outcodes.json')
outcodes_array = json.load(outcodes_file)

record_count = 0

for outcode in outcodes_array:
    print("Fetching data for " + outcode)
    datasource = PricesDataSource(outcode)
    datasource.run_query()

    try:
        results = datasource.get_results_dictionary()
        output_file = open(path + '/data/' + outcode.lower() + '.json', 'w')
        json.dump(results, output_file, sort_keys=True)
        print("File " + output_file.name + " created and written to")
        record_count += 1

    except PricesDataSourceError as error:
        print("An error occured: " + str(error))

print(str(record_count) + " records created")