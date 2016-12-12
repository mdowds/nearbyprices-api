import unittest
from unittest.mock import patch
from datasource.landregistryinterface import LandRegistryInterface, LandRegistryInterfaceError
from datasource.landregistryquery import LandRegistryQuery


class LandRegistryInterfaceTests(unittest.TestCase):

    @patch("datasource.landregistryinterface.SPARQLWrapper")
    def test_runQuery_callsSparqlSetQuery_WithQueryString(self, mock_sparql):
        lrq = LandRegistryQuery("WC2N")
        query_string = lrq.get_querystring()
        lri = LandRegistryInterface(query_string)
        lri.run_query()

        mock_sparql.return_value.setQuery.assert_called_once_with(query_string)

    @patch("datasource.landregistryinterface.SPARQLWrapper")
    def test_runQuery_callsSparqlQueryAndConvert(self, mock_sparql):
        lrq = LandRegistryQuery("WC2N")
        query_string = lrq.get_querystring()
        lri = LandRegistryInterface(query_string)
        lri.run_query()

        self.assertTrue(mock_sparql.return_value.queryAndConvert.called)

    @patch("datasource.landregistryinterface.SPARQLWrapper")
    def test_runQuery_ReturnsCorrectResponse(self, mock_sparql):
        lrq = LandRegistryQuery("WC2N")
        queryString = lrq.get_querystring()
        lri = LandRegistryInterface(queryString)

        expected = {"response":"response"}
        mock_sparql.return_value.queryAndConvert.return_value = expected
        actual = lri.run_query()

        self.assertEqual(actual, expected)

    def testRunQuery_WithEmptyQuery_Raises(self):
        lrq = LandRegistryQuery("")
        query_string = lrq.get_querystring()
        lri = LandRegistryInterface(query_string)

        self.assertRaises(LandRegistryInterfaceError, lri.run_query)
