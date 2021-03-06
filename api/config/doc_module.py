# -*- coding: utf-8 -*-

from flasgger import Swagger
from injector import Module


class DocModule(Module):
    """Configure the Swagger Doc."""

    def __init__(self, app):
        self.app = app

    def configure(self, binder):
        self.app.config['SWAGGER'] = {
            'title': 'Data API',
            'uiversion': 3
        }

        template = {
            "swagger": "2.0",
            "info": {
                'title': 'Data API',
                "description":
                    """
Data API for Data Integration team.                            
                               
See original [Data Integration challenge in NeowayLabs](https://github.com/NeowayLabs/data-integration-challenge).
                               
See DATA API - Online:  
[http://neoway.marcospereirajr.com.br/](http://neoway.marcospereirajr.com.br/)
                    """,
                "contact": {
                    "responsibleOrganization": "Yawoen",
                },
                "version": "1.0.0."
            }
        }

        swagger_config = {
            "headers": [
            ],
            "specs": [
                {
                    "endpoint": 'apispec',
                    "route": '/apispec.json',
                    "rule_filter": lambda rule: True,  # all in
                    "model_filter": lambda tag: True,  # all in
                }
            ],
            "static_url_path": "/flasgger_static",
            "swagger_ui": True,
            "specs_route": "/"
        }

        Swagger(self.app, template=template, config=swagger_config)
