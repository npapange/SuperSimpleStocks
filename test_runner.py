#!/usr/bin/python

import logging.config
import unittest

from tests import test_stock, test_trade_record, test_stock_exchange  # , test_rest_api

__author__ = 'Nikitas Papangelopoulos'

"""
A simple script to run all tests.
"""

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

suite = unittest.TestSuite()

suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(test_stock))
suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(test_trade_record))
suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(test_stock_exchange))
# suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(test_rest_api))

unittest.TextTestRunner().run(suite)
