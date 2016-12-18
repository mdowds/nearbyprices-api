import unittest
from unittest.mock import patch
from datasource.landregistryqueryfactory import LandRegistryQueryFactory


class LandRegistryQueryFactoryTests(unittest.TestCase):

    @patch("datasource.landregistryqueryfactory.LandRegistryQuery")
    def test_mainQuery_callsLRQuery(self, mock_lrq):
        LandRegistryQueryFactory.main_query("WC2N")
        lrq_obj = mock_lrq.return_value

        # Base query calls
        mock_lrq.assert_called_once_with("WC2N")
        self.assertTrue(lrq_obj.add_averageprice.called)
        self.assertTrue(lrq_obj.add_transactioncount.called)

        # Main query calls
        self.assertTrue(lrq_obj.add_town.called)
        lrq_obj.add_year_range.assert_called_once_with(1, 0)

        self.assertTrue(lrq_obj.get_querystring.called)

    @patch("datasource.landregistryqueryfactory.LandRegistryQuery")
    def test_mainQuery_returnsCorrectQuery(self, mock_lrq):
        mock_lrq.return_value.get_querystring.return_value = "Main query"
        query = LandRegistryQueryFactory.main_query("WC2N")

        self.assertEqual(query, "Main query")

    @patch("datasource.landregistryqueryfactory.LandRegistryQuery")
    def test_typeQuery_callsLRQuery(self, mock_lrq):
        LandRegistryQueryFactory.type_query("WC2N")
        lrq_obj = mock_lrq.return_value

        # Base query calls
        mock_lrq.assert_called_once_with("WC2N")
        self.assertTrue(lrq_obj.add_averageprice.called)
        self.assertTrue(lrq_obj.add_transactioncount.called)

        # Type query calls
        lrq_obj.add_year_range.assert_called_once_with(1, 0)
        self.assertTrue(lrq_obj.add_propertytype_select.called)
        self.assertTrue(lrq_obj.add_propertytype_where.called)
        lrq_obj.add_groupby.assert_called_once_with("type")

    @patch("datasource.landregistryqueryfactory.LandRegistryQuery")
    def test_typeQuery_returnsCorrectQuery(self, mock_lrq):
        mock_lrq.return_value.get_querystring.return_value = "Type query"
        query = LandRegistryQueryFactory.main_query("WC2N")

        self.assertEqual(query, "Type query")