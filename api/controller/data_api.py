# -*- coding: utf-8 -*-

from flask_restful import Resource


class DataAPI(Resource):

    def get(self):
        return {'data': 'test'}
