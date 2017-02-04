#!/usr/bin/python
import logging.config

from api import rest_api

__author__ = 'Nikitas Papangelopoulos'

# Getting the logging settings
logging.config.fileConfig('/SuperSimpleStocks/logging.conf', disable_existing_loggers=False)
# running the REST API server.
rest_api.app.run()
