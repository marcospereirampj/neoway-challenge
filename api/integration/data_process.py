# -*- coding: utf-8 -*-

import hashlib

from elasticsearch import Elasticsearch, helpers

from config.default import Config
from controller.custom.custom_api_error import ProcessFileError, InitialImportError


class DataProcess:

    def __init__(self):
        self._elastic_search = Elasticsearch([{'host': Config.ELASTICSEARCH_HOST, 'port': Config.ELASTICSEARCH_PORT}])
        self._document_type = Config.ELASTICSEARCH_DOCUMENT_TYPE
        self._index = Config.ELASTICSEARCH_INDEX
        self._elastic_search.indices.create(index=self._index, ignore=400)

    def retrieve(self, search, scroll_id=None):
        return self._read_database(search, scroll_id)

    def restore(self, input_file_path):
        """
        Read a file, process and return dict with values.

        :param input_file_path: File path
        :return: True if successful restore
        """
        is_header = True
        headers = []
        data_bulk = []

        if self._count_database() > 0:
            raise InitialImportError()

        try:
            # Read largest files
            with open(input_file_path, 'r') as file_object:
                for line in file_object:
                    if is_header:
                        headers = self._process_header(line)
                        is_header = False
                    else:
                        data = self._process_line(line, headers)
                        data_bulk.append(data)

            self._insert_bulk_database(data_bulk)

        except Exception as err:
            raise ProcessFileError()

        return "File successfully processed."

    def update(self, input_file_path):
        """
        Read a file, process and return dict with values.

        :param input_file_path: File path
        :return: True if successful restore
        """
        is_header = True
        headers = []

        try:
            # Read largest files
            with open(input_file_path, 'r') as file_object:
                for line in file_object:
                    if is_header:
                        headers = self._process_header(line)
                        is_header = False
                    else:
                        self._update_database(self._process_line(line, headers))

        except Exception as err:
            raise ProcessFileError()

        return "File successfully processed."

    def _process_header(self, line):
        """
        Process de header read from CSV file.

        :param line: header line.
        :return: values.
        """
        return [i.strip().lower() for i in line.split(';')]

    def _process_line(self, line, headers):
        """
        Process a line read from CSV file.

        :param line: line from CSV file.
        :param headers: keys for result dict
        :return: values
        """
        fields = [i.strip() for i in line.split(';')]

        if len(headers) == len(fields):
            result = {}
            keys = []

            for item, field_name in enumerate(headers):
                result[field_name] = fields[item]

                if field_name.lower() in ['name', 'addresszip']:
                    keys.append(str(fields[item]))

            result['website'] = result['website'] if result.get('website') else None
            result['hash_object'] = self._create_hash_line(keys)

            return result

        return None

    def _create_hash_line(self, keys):
        """
        Create a hash identification for line

        :param keys: keys for hash generation.
        :return: hash
        """

        hash = hashlib.sha256(''.join(keys).encode('utf-8'))
        return hash.hexdigest()

    def _insert_bulk_database(self, data):

        actions = [
            {
                "_index": self._index,
                "_type": self._document_type,
                "_source": item,
                "_id": item['hash_object']
            }
            for item in data
        ]

        helpers.bulk(self._elastic_search, actions)

    def _update_database(self, data):
        try:
            self._elastic_search.update(index=self._index,
                                        doc_type=self._document_type,
                                        id=data['hash_object'],
                                        body={"doc": data})
        except Exception as err:
            pass

        return

    def _read_database(self, search, scroll_id):

        if not scroll_id:
            result = self._elastic_search.search(index=self._index,
                                                 doc_type=self._document_type,
                                                 body=self._get_query_dsl(search),
                                                 **{"scroll": "1m", "size": 100})
        else:
            result = self._elastic_search.scroll(scroll='1m', scroll_id=scroll_id)

        response = {
            "data": [self._format_response(result) for result in result['hits']['hits']],
            "count": result['hits']['total'],
            "scroll": result['_scroll_id']
        }

        return response

    def _count_database(self):
        count = self._elastic_search.count(index=self._index, doc_type=self._document_type)
        return count["count"]

    def _get_query_dsl(self, search):
        query_dsl = None

        if search:
            query_dsl = {
                "_source": ["name", "addresszip", "website"],
                "query": {
                    "match": {
                        "name": search
                    }
                }
            }

        return query_dsl

    def _format_response(self, data):
        response_formatted = data['_source']
        response_formatted.update({'id': data['_id']})
        return response_formatted
