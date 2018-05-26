# -*- coding: utf-8 -*-

"""Test Integration Layer"""

from unittest import TestCase, mock

from config.default import Config
from controller.custom.custom_api_error import ConnectionElasticSearchError, ProcessFileError
from integration.data_process import DataProcess


class DataProcessTest(TestCase):
    """Test Data Process Class"""

    @classmethod
    def setUpClass(cls):
        cls._data_process = DataProcess()

    def test_retrieve_success(self):
        """ Tests success of the process retrieves all data. """

        elastic_mock_result = {
            "_scroll_id": "next_page_hash",
            "hits": {
                "total": 2,
                "hits": [
                    {
                        "_id": "b3a5f3b3f59aae1c92a99c0b57964c9b8324c6abbc66edb8ba6bc1dfdbdf7de9",
                        "_source": {
                            "zip": "11111",
                            "website": "http://www.yawoen.com/locations/pennsylvania/lancaster/17602/16738",
                            "name": "yawoen"
                        }
                    },
                    {
                        "_id": "b3a5f3b3f59aae1c92a99c0b57964c9b8324c6abbc66edb8ba6bc1dfdbdf7de9",
                        "_source": {
                            "zip": "22222",
                            "website": "http://www.yawoen.com/locations/pennsylvania/lancaster/17602/16738",
                            "name": "group"
                        }
                    }

                ]
            }
        }

        self._data_process._elastic_search.search = mock.MagicMock(return_value=elastic_mock_result)

        result = self._data_process.retrieve(name=None, addresszip=None)

        self.assertEqual(3, len(result.keys()))
        self.assertEqual(['count', 'data', 'scroll'], sorted(result.keys()))
        self.assertEqual(2, result['count'])
        self.assertEqual("11111", result['data'][0]['zip'])
        self.assertEqual("http://www.yawoen.com/locations/pennsylvania/lancaster/17602/16738",
                         result['data'][0]['website'])
        self.assertEqual("yawoen", result['data'][0]['name'])

    def test_retrieve_success_by_name(self):
        """ Tests success of the process retrieves data (search by name). """

        elastic_mock_result = {
            "_scroll_id": "next_page_hash",
            "hits": {
                "total": 1,
                "hits": [
                    {
                        "_id": "b3a5f3b3f59aae1c92a99c0b57964c9b8324c6abbc66edb8ba6bc1dfdbdf7de9",
                        "_source": {
                            "zip": "11111",
                            "website": "http://www.yawoen.com/locations/pennsylvania/lancaster/17602/16738",
                            "name": "yawoen"
                        }
                    }
                ]
            }
        }

        self._data_process._elastic_search.search = mock.MagicMock(return_value=elastic_mock_result)

        result = self._data_process.retrieve(name='yawoen', addresszip=None)

        self.assertEqual(3, len(result.keys()))
        self.assertEqual(['count', 'data', 'scroll'], sorted(result.keys()))
        self.assertEqual("11111", result['data'][0]['zip'])
        self.assertEqual("http://www.yawoen.com/locations/pennsylvania/lancaster/17602/16738",
                         result['data'][0]['website'])
        self.assertEqual("yawoen", result['data'][0]['name'])

    def test_retrieve_success_by_zip(self):
        """ Tests success of the process retrieves data (search by zip). """

        elastic_mock_result = {
            "_scroll_id": "next_page_hash",
            "hits": {
                "total": 1,
                "hits": [
                    {
                        "_id": "b3a5f3b3f59aae1c92a99c0b57964c9b8324c6abbc66edb8ba6bc1dfdbdf7de9",
                        "_source": {
                            "zip": "11111",
                            "website": "http://www.yawoen.com/locations/pennsylvania/lancaster/17602/16738",
                            "name": "yawoen"
                        }
                    }
                ]
            }
        }

        self._data_process._elastic_search.search = mock.MagicMock(return_value=elastic_mock_result)

        result = self._data_process.retrieve(name=None, addresszip='1111')

        self.assertEqual(3, len(result.keys()))
        self.assertEqual(['count', 'data', 'scroll'], sorted(result.keys()))
        self.assertEqual("11111", result['data'][0]['zip'])
        self.assertEqual("http://www.yawoen.com/locations/pennsylvania/lancaster/17602/16738",
                         result['data'][0]['website'])
        self.assertEqual("yawoen", result['data'][0]['name'])

    def test_retrieve_success_by_name_and_zip(self):
        """ Tests success of the process retrieves data (search by name and zip). """

        elastic_mock_result = {
            "_scroll_id": "next_page_hash",
            "hits": {
                "total": 1,
                "hits": [
                    {
                        "_id": "b3a5f3b3f59aae1c92a99c0b57964c9b8324c6abbc66edb8ba6bc1dfdbdf7de9",
                        "_source": {
                            "zip": "11111",
                            "website": "http://www.yawoen.com/locations/pennsylvania/lancaster/17602/16738",
                            "name": "yawoen"
                        }
                    }
                ]
            }
        }

        self._data_process._elastic_search.search = mock.MagicMock(return_value=elastic_mock_result)

        result = self._data_process.retrieve(name='yawoen', addresszip='11111')

        self.assertEqual(3, len(result.keys()))
        self.assertEqual(['count', 'data', 'scroll'], sorted(result.keys()))
        self.assertEqual("11111", result['data'][0]['zip'])
        self.assertEqual("http://www.yawoen.com/locations/pennsylvania/lancaster/17602/16738",
                         result['data'][0]['website'])
        self.assertEqual("yawoen", result['data'][0]['name'])

    def test_retrieve_success_next_by_name_and_zip(self):
        """ Tests success of the process retrieves next page (search by name and zip). """

        elastic_mock_result = {
            "_scroll_id": "next_page_hash",
            "hits": {
                "total": 1,
                "hits": [
                    {
                        "_id": "b3a5f3b3f59aae1c92a99c0b57964c9b8324c6abbc66edb8ba6bc1dfdbdf7de9",
                        "_source": {
                            "zip": "22222",
                            "website": "http://www.yawoen.com/locations/pennsylvania/lancaster/17602/16738",
                            "name": "yawoen"
                        }
                    }
                ]
            }
        }

        self._data_process._elastic_search.scroll = mock.MagicMock(return_value=elastic_mock_result)

        result = self._data_process.retrieve(name='yawoen', addresszip='22222', scroll_id='next_page_hash')

        self.assertEqual(3, len(result.keys()))
        self.assertEqual(['count', 'data', 'scroll'], sorted(result.keys()))
        self.assertEqual("22222", result['data'][0]['zip'])
        self.assertEqual("http://www.yawoen.com/locations/pennsylvania/lancaster/17602/16738",
                         result['data'][0]['website'])
        self.assertEqual("yawoen", result['data'][0]['name'])

    def test_retrieve_not_found_by_name_and_zip(self):
        """ Not found data test. """

        elastic_mock_result = {
            "_scroll_id": "next_page_hash",
            "hits": {
                "total": 0,
                "hits": []
            }
        }

        self._data_process._elastic_search.search = mock.MagicMock(return_value=elastic_mock_result)

        result = self._data_process.retrieve(name='yawoen', addresszip='22222')

        self.assertEqual(3, len(result.keys()))
        self.assertEqual(['count', 'data', 'scroll'], sorted(result.keys()))
        self.assertEqual(0, len(result['data']))
        self.assertEqual(0, result['count'])

    def test_connection_error(self):
        """ Connection error test. """

        Config.ELASTICSEARCH_HOST = 'invaliddomain'

        try:
            _data_process = DataProcess()
        except Exception as err:
            self.assertEqual(True, isinstance(err, ConnectionElasticSearchError))

    def test_success_restore(self):
        """ Tests file recovery successfully. """

        f = open('/tmp/inputData.csv', 'w')
        f.write("name;addressZip\n")
        f.write("group;78229\n")
        f.write("foundation;94002\n")
        f.write("yawoen group;30078\n")
        f.close()

        self._data_process._count_database = mock.MagicMock(return_value=0)
        self._data_process._insert_bulk_database = mock.MagicMock(return_value=None)

        result = self._data_process.restore('/tmp/inputData.csv')
        self.assertEqual("File successfully processed.", result)

    def test_ignored_invalid_lines_restore(self):
        """ Tests file recovery successfully (ignored invalid lines). """

        f = open('/tmp/inputData.csv', 'w')
        f.write("name;addressZip\n")
        f.write("group;78229\n")
        f.write("foundation\n")
        f.write("yawoen group;30078\n")
        f.close()

        self._data_process._count_database = mock.MagicMock(return_value=0)
        self._data_process._insert_bulk_database = mock.MagicMock(return_value=None)

        # Ignored invalid lines
        result = self._data_process.restore('/tmp/inputData.csv')
        self.assertEqual("File successfully processed.", result)

    def test_fail_process_restore(self):
        """File recovery fail test. """

        self._data_process._count_database = mock.MagicMock(return_value=0)
        self._data_process._insert_bulk_database = mock.MagicMock(return_value=None)

        try:
            result = self._data_process.restore('/tmp/inputDataNotFound.csv')
        except Exception as err:
            self.assertEqual(True, isinstance(err, ProcessFileError))

    def test_success_update(self):
        """ Tests update database successfully (ignored invalid lines). """

        f = open('/tmp/inputDataUpdate.csv', 'w')
        f.write("name;addressZip;website\n")
        f.write("group;78229;http://group.com\n")
        f.write("foundation;94002;http://foundation.com\n")
        f.write("yawoen group;30078;http://yawoen.com\n")
        f.close()

        self._data_process._update_database = mock.MagicMock(return_value=None)

        result = self._data_process.update('/tmp/inputDataUpdate.csv')
        self.assertEqual("File successfully processed.", result)

    def test_fail_process_update(self):
        """Update database fail test. """

        self._data_process._update_database = mock.MagicMock(return_value=None)

        try:
            result = self._data_process.update('/tmp/inputDataNotFound.csv')
        except Exception as err:
            self.assertEqual(True, isinstance(err, ProcessFileError))
