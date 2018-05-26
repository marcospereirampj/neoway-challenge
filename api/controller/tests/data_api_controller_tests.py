# -*- coding: utf-8 -*-
""" Test controller layer """

import json

from unittest import TestCase, mock

from io import BytesIO

from config import create_app

app = create_app('config.default.Config')


class DataApiControllerTest(TestCase):
    """Test Data Process Class"""

    @classmethod
    def setUpClass(cls):
        cls._app = app.test_client()
        cls._headers = {'Content-Type': 'application/json'}

    @mock.patch("integration.data_process.DataProcess._read_database")
    def test_get_all_results_success(self, mock_elasticsearch):
        mock_elasticsearch.return_value = {
            "count": 2,
            "scroll": "next_page_hash",
            "data": [
                {
                    "id": "ffa4a5e5666b88c493a1a55a50f58ac16116b628e15a54d2e415d883bba82dfe",
                    "zip": "30078",
                    "name": "dwight harrison vw",
                    "website": "http://harrison.com"
                },
                {
                    "id": "50c0480283ded7ad6fc28edfcbf637a02919da98961f195a812183d36c45fcc4",
                    "zip": "33178",
                    "name": "linda group usa llc",
                    "website": "http://linda.com"
                }
            ]
        }

        response = self._app.get('/data-integration', headers=self._headers)
        response_json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(3, len(response_json))
        self.assertEqual(2, response_json['count'])
        self.assertEqual(2, len(response_json['data']))

    @mock.patch("integration.data_process.DataProcess._read_database")
    def test_get_results_by_name_and_zip_success(self, mock_elasticsearch):
        mock_elasticsearch.return_value ={
            "count": 1,
            "scroll": "next_page_hash",
            "data": [
                {
                    "id": "ffa4a5e5666b88c493a1a55a50f58ac16116b628e15a54d2e415d883bba82dfe",
                    "zip": "30078",
                    "name": "dwight harrison vw",
                    "website": "http://harrison.com"
                }
            ]
        }

        response = self._app.get('/data-integration?name=dwight&zip=30078', headers=self._headers)
        response_json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(3, len(response_json))
        self.assertEqual(1, response_json['count'])
        self.assertEqual(1, len(response_json['data']))

    @mock.patch("integration.data_process.DataProcess._read_database")
    def test_get_not_found(self, mock_elasticsearch):
        mock_elasticsearch.return_value = {
            "count": 0,
            "scroll": "next_page_hash",
            "data": []
        }

        response = self._app.get('/data-integration?name=dwight&zip=30078', headers=self._headers)
        response_json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(3, len(response_json))
        self.assertEqual(0, response_json['count'])
        self.assertEqual(0, len(response_json['data']))

    @mock.patch("integration.data_process.DataProcess._count_database")
    def test_post_initial_import_error(self, mock_elasticsearch_count):
        mock_elasticsearch_count.return_value = 10

        f = open('/tmp/inputData.csv', 'w')
        f.write("name;addressZip\n")
        f.write("group;78229\n")
        f.write("foundation;10022\n")
        f.write("yawoen group;30078\n")
        f.close()

        response = self._app.post('/data-integration',
                                  headers={'Content-Type': 'multipart/form-data'},
                                  data={'file': (BytesIO(b'my file contents'), 'inputData.csv')})

        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(2, len(response_json))
        self.assertEqual(500, response_json['status'])
        self.assertEqual("There is data in the database.", response_json['message'])

    @mock.patch("integration.data_process.DataProcess._insert_bulk_database")
    @mock.patch("integration.data_process.DataProcess._count_database")
    def test_post_success(self, mock_elasticsearch_count, mock_elasticsearch_insert):
        mock_elasticsearch_count.return_value = 0
        mock_elasticsearch_insert.return_value = None

        f = open('/tmp/inputData.csv', 'w')
        f.write("name;addressZip\n")
        f.write("group;78229\n")
        f.write("foundation;10022\n")
        f.write("yawoen group;30078\n")
        f.close()

        response = self._app.post('/data-integration',
                                  headers={'Content-Type': 'multipart/form-data'},
                                  data={'file': (BytesIO(b'my file contents'), 'inputData.csv')})

        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(2, len(response_json))
        self.assertEqual(200, response_json['status'])
        self.assertEqual("File successfully processed.", response_json['message'])

    @mock.patch("integration.data_process.DataProcess._update_database")
    @mock.patch("integration.data_process.DataProcess._count_database")
    def test_put_success(self, mock_elasticsearch_count, mock_elasticsearch_update):
        mock_elasticsearch_count.return_value = 0
        mock_elasticsearch_update.return_value = None

        f = open('/tmp/inputData.csv', 'w')
        f.write("name;addressZip\n")
        f.write("group;78229\n")
        f.write("foundation;10022\n")
        f.write("yawoen group;30078\n")
        f.close()

        response = self._app.put('/data-integration',
                                 headers={'Content-Type': 'multipart/form-data'},
                                 data={'file': (BytesIO(b'my file contents'), 'inputData.csv')})

        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(2, len(response_json))
        self.assertEqual(200, response_json['status'])
        self.assertEqual("File successfully processed.", response_json['message'])