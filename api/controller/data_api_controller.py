# -*- coding: utf-8 -*-

import werkzeug

from flasgger import swag_from
from flask_restful import Resource, reqparse

from integration.data_process import DataProcess


class DataApiController(Resource):
    """
    Class responsible for API. Process HTTP requests.
    """

    def __init__(self, directory='/tmp/'):
        self._data_process = DataProcess()
        self._directory = directory

    def _save_file(self, parse):
        """
        Save file in file storage

        :param parse: parse from request
        :return: filename saved
        """

        parse.add_argument('file', type=werkzeug.FileStorage, location='files')
        args = parse.parse_args()

        csv_file = args['file']
        csv_file.save(self._directory + csv_file.filename)
        csv_file.close()

        return csv_file.filename

    @swag_from('swagger/data_api_controller_post.yml')
    def post(self):
        """
        Process data from CSV file (initial load data).

        :return Operating result.
        """
        parse = reqparse.RequestParser()
        filename = self._save_file(parse)
        result = self._data_process.restore(self._directory + filename)

        return {'message': result, 'status': 200}

    @swag_from('swagger/data_api_controller_put.yml')
    def put(self):
        """
        Process data from CSV file (database update).

        :return Operating result.
        """
        parse = reqparse.RequestParser()
        filename = self._save_file(parse)
        result = self._data_process.update(self._directory + filename)

        return {'message': result, 'status': 200}

    @swag_from('swagger/data_api_controller_get.yml')
    def get(self):
        """
        Retrieve objects from database.

        :return: List of objects from the database.
        """

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='args', required=False)
        parser.add_argument('zip', type=str, location='args', required=False)
        parser.add_argument('scroll_id', type=str, location='args', required=False)
        args = parser.parse_args()

        return self._data_process.retrieve(args['name'], args['zip'], args.get('scroll_id'))
