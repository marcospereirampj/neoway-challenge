# -*- coding: utf-8 -*-

from flask_restful import HTTPException


class ProcessFileError(HTTPException):
    code = 500


custom_errors = {
    'ProcessFileError': {
        'message': "Failed to process file.",
        'status': 500,
    }
}