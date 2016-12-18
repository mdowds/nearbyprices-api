import unittest
from unittest.mock import patch
import json
import os.path
from datasource.pricesdatasource import PricesDataSource


class PricesDataSourceTests(unittest.TestCase):

    PATH = os.path.dirname(__file__)
    MAIN_QUERY = "main"
    TYPE_QUERY = "type"
    CHANGE_QUERY = "change"

    def setUp(self):
        self.pds = PricesDataSource("WC2N")

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
    @patch("datasource.pricesdatasource.LandRegistryQueryFactory")
    def test_runQuery_callsLRInterface_WithChangeQuery(self, mock_factory, mock_lri):
        mock_factory.change_query.return_value = self.CHANGE_QUERY
        self.pds.run_query()

        mock_lri.run_query.assert_any_call(self.CHANGE_QUERY)

    @patch("datasource.pricesdatasource.LandRegistryInterface")
    @patch("datasource.pricesdatasource.LandRegistryInterface")
    def test_runQuery_setsCorrectReturnValues(self, mock_factory, mock_lri):
        mock_factory.main_query.return_value = self.MAIN_QUERY
        mock_factory.type_query.return_value = self.TYPE_QUERY
        mock_factory.change_query.return_value = self.CHANGE_QUERY
        mock_lri.run_query.side_effect = self.mock_runquery

        self.pds.run_query()
        self.assertEqual(self.pds.area_name, "London")
        self.assertEqual(self.pds.average_price, 500000)
        self.assertEqual(self.pds.transaction_count, 1000)

    @patch("datasource.pricesdatasource.LandRegistryInterface")
    @patch("datasource.pricesdatasource.LandRegistryQueryFactory")
    def test_runQuery_setsCorrectTypeAverages(self, mock_factory, mock_lri):
        mock_factory.main_query.return_value = self.MAIN_QUERY
        mock_factory.type_query.return_value = self.TYPE_QUERY
        mock_factory.change_query.return_value = self.CHANGE_QUERY
        mock_lri.run_query.side_effect = self.mock_runquery

        self.pds.run_query()

        self.assertEqual(self.pds.detached_average, 300000)
        self.assertEqual(self.pds.semi_detached_average, 205000)
        self.assertEqual(self.pds.terraced_average, 200000)
        self.assertEqual(self.pds.flat_average, 135000)

    # @patch("datasource.pricesdatasource.LandRegistryInterface")
    # @patch("datasource.pricesdatasource.LandRegistryQueryFactory")
    # def test_runQuery_withErrorInResponse_Raises(self, mock_factory, mock_lri):

    # Helper methods

    @classmethod
    def get_sample_data(cls, name):
        path = os.path.join(cls.PATH, "testdata/")
        file = open(path + name + ".json")
        return json.load(file)

    @classmethod
    def mock_runquery(cls, query):
        if query == cls.TYPE_QUERY:
            return cls.get_sample_data("lrtypes")
        else:
            return cls.get_sample_data("lrmain")
