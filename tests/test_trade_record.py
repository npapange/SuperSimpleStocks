#!/usr/bin/python

import unittest
import logging.config

from simple_stock_exchange import Stock, TradeRecord, StockExchange
from datetime import datetime

__author__ = 'Nikitas Papangelopoulos'

logging.config.fileConfig('/SuperSimpleStocks/logging.conf', disable_existing_loggers=False)


class TestTrade(unittest.TestCase):

    def test_simple(self):
        trade = TradeRecord(StockExchange('test'), 'TEA', '500', 'sell', '150')
        time_stamp = datetime.strptime(str(datetime.now())[:-10], '%Y-%m-%d %H:%M')
        self.assertEqual(trade.stock_symbol, 'TEA')
        self.assertEqual(trade.quantity, 500.0)
        self.assertEqual(trade.trade_type, 'sell')
        self.assertEqual(trade.traded_price, 150)
        self.assertEqual(str(trade.time_stamp)[:-3], str(time_stamp)[:-3])  # removing seconds
        self.assertTrue(trade.created_successfully)

    def test_time_stamp(self):
        trade = TradeRecord(StockExchange('test'), 'TEA', '500', 'sell', '150', '2017-02-05 22:14:39')
        self.assertEqual(trade.stock_symbol, 'TEA')
        self.assertEqual(trade.quantity, 500.0)
        self.assertEqual(trade.trade_type, 'sell')
        self.assertEqual(trade.traded_price, 150)
        self.assertEqual(trade.time_stamp, datetime.strptime('2017-02-05 22:14:39', '%Y-%m-%d %H:%M:%S'))
        self.assertTrue(trade.created_successfully)

    def test_exceptions(self):
        trade = TradeRecord('test', 'TEA', 'test1', 'test2', 'test3', 'test4')
        self.assertFalse(trade.created_successfully)

    def test_type_mismatch(self):
        stock = Stock('GIN', 'preferred', '8', '100')
        self.assertEqual(stock.stock_type, 'preferred')
        self.assertIsNone(stock.fixed_dividend)
        self.assertFalse(stock.created_successfully)
