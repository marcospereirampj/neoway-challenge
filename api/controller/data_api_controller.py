# -*- coding: utf-8 -*-

import werkzeug
from flasgger import swag_from

from flask_restful import Resource, reqparse

from integration.data_process import DataProcess


class DataApiController(Resource):

    def __init__(self, directory='files/'):
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
        Process data from CSV file.
        """
        parse = reqparse.RequestParser()
        filename = self._save_file(parse)
        result = self._data_process.restore(self._directory + filename)

        return {'message': result, 'status': 200}

    @swag_from('swagger/data_api_controller_get.yml')
    def get(self):
        return self._data_restore.restore("/media/DATA/workspace/personal/neoway-challenge/data/q1_catalog.csv")