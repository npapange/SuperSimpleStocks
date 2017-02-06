#!/usr/bin/python

import logging.config
import unittest

from simple_stock_exchange import Stock, StockExchange

__author__ = 'Nikitas Papangelopoulos'

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)


class TestStock(unittest.TestCase):
    def test_simple(self):
        stock = Stock('TEA', 'common', '0', '100')
        self.assertEqual(stock.stock_symbol, 'TEA')
        self.assertEqual(stock.stock_type, 'common')
        self.assertEqual(stock.last_dividend, 0.0)
        self.assertEqual(stock.par_value, 100.0)
        self.assertTrue(stock.created_successfully)

    def test_fixed_dividend(self):
        stock = Stock('GIN', 'preferred', '8', '100', '2%')
        self.assertEqual(stock.stock_symbol, 'GIN')
        self.assertEqual(stock.stock_type, 'preferred')
        self.assertEqual(stock.last_dividend, 8.0)
        self.assertEqual(stock.fixed_dividend, 0.02)
        self.assertEqual(stock.par_value, 100.0)
        self.assertTrue(stock.created_successfully)

    def test_fixed_dividend1(self):
        stock = Stock('GIN', 'preferred', '8', '100', '0.02')
        self.assertEqual(stock.stock_symbol, 'GIN')
        self.assertEqual(stock.stock_type, 'preferred')
        self.assertEqual(stock.last_dividend, 8.0)
        self.assertEqual(stock.fixed_dividend, 0.02)
        self.assertEqual(stock.par_value, 100.0)
        self.assertTrue(stock.created_successfully)

    def test_fixed_dividend_exchange(self):
        stock_exchange = StockExchange('test')
        stock = Stock('GIN', 'preferred', '8', '100', '0.02', stock_exchange)
        self.assertEqual(stock.stock_symbol, 'GIN')
        self.assertEqual(stock.stock_type, 'preferred')
        self.assertEqual(stock.last_dividend, 8.0)
        self.assertEqual(stock.fixed_dividend, 0.02)
        self.assertEqual(stock.par_value, 100.0)
        self.assertEqual(stock.current_stock_exchange, stock_exchange)
        self.assertTrue(stock.created_successfully)

    def test_exceptions(self):
        stock = Stock('GIN', 'other', 'test', 'test1', 'test.3', 'stock_exchange')
        self.assertFalse(stock.created_successfully)

    def test_exceptions1(self):
        stock = Stock('GIN', 'other', 'test', 'test1', 'test3', 'stock_exchange')
        self.assertFalse(stock.created_successfully)

    def test_type_mismatch(self):
        stock = Stock('GIN', 'preferred', '8', '100')
        self.assertEqual(stock.stock_type, 'preferred')
        self.assertIsNone(stock.fixed_dividend)
        self.assertFalse(stock.created_successfully)
