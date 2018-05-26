# -*- coding: utf-8 -*-

from flask.app import Flask
from flask_injector import FlaskInjector
from injector import Injector

from config.app_module import AppModule
from config.doc_module import DocModule


def create_app(config_name):
    """
    Create Flask configuration

    :param config_name: File on package config
    :return: Flask aplication

    """

    app = Flask(__name__)
    app.config.from_object(config_name)

    injector = Injector([DocModule(app), AppModule(app)])
    FlaskInjector(app=app, injector=injector)

    return app
