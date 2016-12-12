from SPARQLWrapper import SPARQLWrapper, JSON


class LandRegistryInterface:
    def __init__(self, query_string):
        self.query = query_string

    def run_query(self):
        sparql = SPARQLWrapper("http://landregistry.data.gov.uk/landregistry/query")
        sparql.setReturnFormat(JSON)
        sparql.setQuery(self.query)

        try:
            results = sparql.queryAndConvert()
            return results
        except:
            raise LandRegistryInterfaceError("Error in running query")


class LandRegistryInterfaceError(Exception):
    pass