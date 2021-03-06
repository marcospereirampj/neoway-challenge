# -*- coding: utf-8 -*-

""" Main configuration module """

import os


class Config:
    """
    Base configuration,
    this class contains most of the variables and default values.

    """
    ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_HOST', 'localhost')
    ELASTICSEARCH_PORT = os.environ.get('ELASTICSEARCH_PORT', '9200')
    ELASTICSEARCH_INDEX = os.environ.get('ELASTICSEARCH_INDEX', 'yawoen')
    ELASTICSEARCH_DOCUMENT_TYPE = os.environ.get('ELASTICSEARCH_DOCUMENT_TYPE', 'catalog')

