# -*- coding: utf-8 -*-

from flask_restful import HTTPException


class ConnectionElasticSearchError(HTTPException):
    code = 500


class ProcessFileError(HTTPException):
    code = 500


class InitialImportError(HTTPException):
    code = 500


custom_errors = {
    'ConnectionElasticSearchError': {
        'message': "Error trying to connect to ElasticSearch.",
        'status': 500,
    },
    'ProcessFileError': {
        'message': "Failed to process file.",
        'status': 500,
    },
    'InitialImportError': {
        'message': "There is data in the database.",
        'status': 500,
    }
}