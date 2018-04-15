import unittest
from unittest.mock import patch
import json
import os.path
from update.datasource.pricesdatasource import PricesDataSource, PricesDataSourceError, LandRegistryInterfaceError


class PricesDataSourceTests(unittest.TestCase):

    PATH = os.path.dirname(__file__)
    MAIN_QUERY = "main"
    TYPE_QUERY = "type"

    def setUp(self):
        self.pds = PricesDataSource("WC2N")

    def tearDown(self):
        self.pds.error = None

    @patch("datasource.pricesdatasource.LandRegistryInterface")
    @patch("datasource.pricesdatasource.LandRegistryQueryFactory")
    def test_runQuery_callsLRInterface_WithMainQuery(self, mock_factory, mock_lri):
        mock_factory.main_query.return_value = self.MAIN_QUERY
        self.pds.run_query()

        mock_lri.run_query.assert_any_call(self.MAIN_QUERY)

    @patch("datasource.pricesdatasource.LandRegistryInterface")
    @patch("datasource.pricesdatasource.LandRegistryQueryFactory")
    def test_runQuery_callsLRInterface_WithTypeQuery(self, mock_factory, mock_lri):
        mock_factory.type_query.return_value = self.TYPE_QUERY
        self.pds.run_query()

        mock_lri.run_query.assert_any_call(self.TYPE_QUERY)

    @patch("datasource.pricesdatasource.LandRegistryInterface")
    @patch("datasource.pricesdatasource.LandRegistryInterface")
    def test_runQuery_setsCorrectReturnValues(self, mock_factory, mock_lri):
        mock_factory.main_query.return_value = self.MAIN_QUERY
        mock_factory.type_query.return_value = self.TYPE_QUERY
        mock_lri.run_query.side_effect = self.mock_runquery

        self.pds.run_query()
        self.assertEqual(self.pds.output['areaName'], "London")
        self.assertEqual(self.pds.output['averagePrice'], 500000)
        self.assertEqual(self.pds.output['transactionCount'], 1000)

    @patch("datasource.pricesdatasource.LandRegistryInterface")
    @patch("datasource.pricesdatasource.LandRegistryQueryFactory")
    def test_runQuery_setsCorrectTypeAverages(self, mock_factory, mock_lri):
        mock_factory.main_query.return_value = self.MAIN_QUERY
        mock_factory.type_query.return_value = self.TYPE_QUERY
        mock_lri.run_query.side_effect = self.mock_runquery

        self.pds.run_query()

        self.assertEqual(self.pds.output['detachedAverage'], 300000)
        self.assertEqual(self.pds.output['semiDetachedAverage'], 205000)
        self.assertEqual(self.pds.output['terracedAverage'], 200000)
        self.assertEqual(self.pds.output['flatAverage'], 135000)


    @patch("datasource.pricesdatasource.LandRegistryInterface")
    @patch("datasource.pricesdatasource.LandRegistryInterface")
    def test_runQuery_WithNoTransactionsReturned_SetsError(self, mock_factory, mock_lri):
        mock_lri.run_query.return_value = {"results": {"bindings": [{"transactionCount": {"value": "0"}}]}}

        self.pds.run_query()
        self.assertEqual(self.pds.error, "No transactions for outcode")

    @patch("datasource.pricesdatasource.LandRegistryInterface")
    @patch("datasource.pricesdatasource.LandRegistryQueryFactory")
    def test_runQuery_withEmptyResponse_SetsError(self, mock_factory, mock_lri):
        mock_lri.run_query.return_value = {"results": {"bindings": []}}
        self.pds.run_query()
        self.assertEqual(self.pds.error, "No results found")

    @patch("datasource.pricesdatasource.LandRegistryInterface")
    @patch("datasource.pricesdatasource.LandRegistryQueryFactory")
    def test_runQuery_whenLRIRaises_SetsError(self, mock_factory, mock_lri):
        mock_lri.run_query.side_effect = LandRegistryInterfaceError("LRI error")
        self.pds.run_query()
        self.assertEqual(self.pds.error, "LRI error")

    @patch("datasource.pricesdatasource.LandRegistryInterface")
    @patch("datasource.pricesdatasource.LandRegistryQueryFactory")
    def test_runQuery_withErrorResponse_SetsError(self, mock_factory, mock_lri):
        mock_lri.run_query.return_value = "Error 400: Parse error etc."
        self.pds.run_query()
        self.assertEqual(self.pds.error, "Error in query")

    def test_getResultsDictionary_ReturnsResults(self):
        expected = { "results": "data" }
        self.pds.output = expected
        self.assertEqual(self.pds.get_results_dictionary(), expected)

    def test_getResultsDictionary_WithErrorSet_Raises(self):
        self.pds.error = "Error"
        self.assertRaises(PricesDataSourceError, self.pds.get_results_dictionary)

    # Helper methods

    @classmethod
    def get_sample_data(cls, name):
        path = os.path.join(cls.PATH, "testdata/")
        with open(path + name + ".json") as file:
            return json.load(file)

    @classmethod
    def mock_runquery(cls, query):
        if query == cls.TYPE_QUERY:
            return cls.get_sample_data("lrtypes")
        else:
            return cls.get_sample_data("lrmain")
