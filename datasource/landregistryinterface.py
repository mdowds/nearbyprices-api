from SPARQLWrapper import SPARQLWrapper, JSON


class LandRegistryInterface:

    @staticmethod
    def run_query(query_string):

        if type(query_string) != str or len(query_string) == 0:
            raise LandRegistryInterfaceError("Invalid query")

        sparql = SPARQLWrapper("http://landregistry.data.gov.uk/landregistry/query")
        sparql.setReturnFormat(JSON)
        sparql.setQuery(query_string)

        try:
            results = sparql.queryAndConvert()
            return results
        except:
            raise LandRegistryInterfaceError("Error in running query")


class LandRegistryInterfaceError(Exception):
    pass