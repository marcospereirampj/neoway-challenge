# -*- coding: utf-8 -*-

"""Test de CRUD Localization Domain"""

from unittest import TestCase, mock

from integration.data_process import DataProcess


class DataProcessTest(TestCase):
    """Test Data Process Class"""

    @classmethod
    def setUpClass(cls):
        cls._data_process = DataProcess()

    def retrieve_success_by_name_test(self):
        elastic_mock_result = {
            "hits": {
                "total": 1,
                "hits": [
                    {
                        "_source": {
                            "zip": "1111",
                            "website": "http://www.yawoen.com/locations/pennsylvania/lancaster/17602/16738",
                            "name": "yawoen"
                        }
                    }
                ]
            }
        }

        self._data_process._read_database = mock.MagicMock(return_value=elastic_mock_result)

        result = self._data_process.retrieve(name='yawoen')

        self.assertEqual(3, len(result.keys()))
        self.assertEqual(['count', 'data', 'scroll'], sorted(result.keys()))

    def restore_test(self):
        pass

    def update_test(self):
        pass