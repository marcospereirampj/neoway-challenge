# -*- coding: utf-8 -*-

import hashlib

from elasticsearch import Elasticsearch, helpers

from config.default import Config
from controller.custom.custom_api_error import ProcessFileError, InitialImportError, ConnectionElasticSearchError


class DataProcess:
    """
    Class responsible to process the CSV file. It's responsible for load initial data in the database,
    update and retrieve data.
    """

    def __init__(self):

        try:
            self._elastic_search = Elasticsearch(
                [{'host': Config.ELASTICSEARCH_HOST, 'port': Config.ELASTICSEARCH_PORT}])
            self._document_type = Config.ELASTICSEARCH_DOCUMENT_TYPE
            self._index = Config.ELASTICSEARCH_INDEX
            self._elastic_search.indices.create(index=self._index, ignore=400)
        except Exception as err:
            raise ConnectionElasticSearchError()

    def retrieve(self, name, addresszip, scroll_id=None):
        """
        Retrieve objects from database.

        :param name: Key for search in name field.
        :param addresszip: Key for search in zip field
        :param scroll_id: Page (or scroll)

        :return: List of objects from the database

        """
        return self._read_database(name, addresszip, scroll_id)

    def restore(self, input_file_path):
        """
        Read a file, process and insert values into the database (initial load).

        :param input_file_path: File path.
        :return: Operation result.
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

                        if data:
                            data_bulk.append(data)

            self._insert_bulk_database(data_bulk)

        except Exception as err:
            raise ProcessFileError()

        return "File successfully processed."

    def update(self, input_file_path):
        """
        Read a file, process and insert values into the database (database update).

        :param input_file_path: File path.
        :return: Operation result.
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
        :return: values (dict)
        """
        fields = [i.strip() for i in line.split(';')]

        if len(headers) == len(fields):
            result = {}
            keys = []

            for item, field_name in enumerate(headers):

                field_name_formatted = field_name.lower() if field_name.lower() != 'addresszip' else 'zip'
                result[field_name_formatted] = fields[item]

                if field_name.lower() in ['name', 'addresszip']:
                    keys.append(str(fields[item]))

            result['website'] = result['website'] if result.get('website') else None
            result['hash_object'] = self._create_hash_line(keys)

            return result

        return None

    def _create_hash_line(self, keys):
        """
        Create a hash code from the line data.

        :param keys: keys for hash generation.
        :return: hash code.
        """

        hash = hashlib.sha256(''.join(keys).encode('utf-8'))
        return hash.hexdigest()

    def _insert_bulk_database(self, data):
        """
        Insert data bulk into the database.

        :param data: data bulk.
        :return:
        """
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
        return

    def _update_database(self, data):
        """
        Update an exists object into the database.

        :param data: object data.
        :return:
        """
        try:
            self._elastic_search.update(index=self._index,
                                        doc_type=self._document_type,
                                        id=data['hash_object'],
                                        body={"doc": data})
        except Exception as err:
            pass

        return

    def _read_database(self, name, addresszip, scroll_id):
        """
        Retrieve objects from database.

        :param name: Key for search in name field.
        :param addresszip: Key for search in zip field
        :param scroll_id: Page (or scroll)

        :return: List of objects from the database
        """

        if not scroll_id:
            result = self._elastic_search.search(index=self._index,
                                                 doc_type=self._document_type,
                                                 body=self._get_query_dsl(name, addresszip),
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
        """
        Count objects in the database.

        :return: the number of objects.
        """
        count = self._elastic_search.count(index=self._index, doc_type=self._document_type)
        return count["count"]

    def _get_query_dsl(self, name, addresszip):
        """
        Create query (DSL).

        :param name: Key for search in name field.
        :param addresszip: Key for search in zip field

        :return: query
        """
        query_dsl = {"_source": ["name", "zip", "website"]}
        must = []

        if name:
            must.append({"match": {"name": name}})

        if addresszip:
            must.append({"match": {"zip": addresszip}})

        if must:
            query_dsl['query'] = {
                "bool": {
                    "must": must
                }
            }

        return query_dsl

    def _format_response(self, data):
        """
        Format response.

        :param data: list of objects
        :return: list of objects formatted.
        """
        response_formatted = data['_source']
        response_formatted.update({'id': data['_id']})
        return response_formatted
