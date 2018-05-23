# -*- coding: utf-8 -*-

from flask_cors.extension import CORS
from injector import Module
from flask_restful import Api

from controller.custom.custom_api_error import custom_errors
from controller.data_api_controller import DataApiController


class AppModule(Module):
    """Configure the application."""

    def __init__(self, app):
        self.app = app
        self.app.url_map.strict_slashes = False
        self.api = Api(app, errors=custom_errors)
        CORS(self.app, resources={r"/*": {"origins": "*"}})

    def configure(self, binder):
        self._configure_endpoints()

    def _configure_endpoints(self):
        """
        Configure endpoints
        """
        self.api.add_resource(DataApiController, '/data-integration')
