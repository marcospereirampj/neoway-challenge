# -*- coding: utf-8 -*-

import hashlib

from elasticsearch import Elasticsearch, helpers

from config.default import Config
from controller.custom.custom_api_error import ProcessFileError


class DataProcess:

    def __init__(self):
        self._elastic_search = Elasticsearch([{'host': Config.ELASTICSEARCH_HOST, 'port': Config.ELASTICSEARCH_PORT}])
        self._document_type = Config.ELASTICSEARCH_DOCUMENT_TYPE
        self._index = Config.ELASTICSEARCH_INDEX
        self._elastic_search.indices.create(index=self._index, ignore=400)

    def restore(self, input_file_path):
        """
        Read a file, process and return dict with values.

        :param input_file_path: File path
        :return: True if successful restore
        """
        is_header = True
        headers = []
        data_bulk = []

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
        return [i.strip() for i in line.split(';')]

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
