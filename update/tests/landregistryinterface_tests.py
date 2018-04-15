import unittest
from unittest.mock import patch
from update.datasource.landregistryinterface import LandRegistryInterface, LandRegistryInterfaceError


class LandRegistryInterfaceTests(unittest.TestCase):

    QUERY_STRING = "Query"

    @patch("datasource.landregistryinterface.SPARQLWrapper")
    def test_runQuery_callsSparqlSetQuery_WithQueryString(self, mock_sparql):
        LandRegistryInterface.run_query(self.QUERY_STRING)
        mock_sparql.return_value.setQuery.assert_called_once_with(self.QUERY_STRING)

    @patch("datasource.landregistryinterface.SPARQLWrapper")
    def test_runQuery_callsSparqlQueryAndConvert(self, mock_sparql):
        LandRegistryInterface.run_query(self.QUERY_STRING)
        self.assertTrue(mock_sparql.return_value.queryAndConvert.called)

    @patch("datasource.landregistryinterface.SPARQLWrapper")
    def test_runQuery_ReturnsCorrectResponse(self, mock_sparql):
        expected = {"response":"response"}
        mock_sparql.return_value.queryAndConvert.return_value = expected
        actual = LandRegistryInterface.run_query(self.QUERY_STRING)

        self.assertEqual(actual, expected)

    def testRunQuery_WithEmptyQuery_Raises(self):
        self.assertRaises(LandRegistryInterfaceError, LandRegistryInterface.run_query, "")

    def testRunQuery_WithNonStringQuery_Raises(self):
        self.assertRaises(LandRegistryInterfaceError, LandRegistryInterface.run_query, 12)
