#!/usr/bin/python

import unittest
import logging.config

from simple_stock_exchange import Stock, TradeRecord, StockExchange

__author__ = 'Nikitas Papangelopoulos'

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)


class TestStockExchange(unittest.TestCase):

    def test_add_new_stock(self):
        stock_exchange = StockExchange('test')
        stock = Stock('GIN', 'preferred', '8', '100', '2%')
        stock_exchange.add_new_stock(stock)
        stock_exchange.add_new_stock(stock)

    def test_remove_stock(self):
        stock_exchange = StockExchange('test')
        stock = Stock('GIN', 'preferred', '8', '100', '2%')
        stock_exchange.add_new_stock(stock)
        stock_exchange.remove_existing_stock(stock)
        stock_exchange.remove_existing_stock(stock)

    def test_remove_stock_by_symbol(self):
        stock_exchange = StockExchange('test')
        stock = Stock('GIN', 'preferred', '8', '100', '2%')
        stock_exchange.add_new_stock(stock)
        stock_exchange.remove_existing_stock_by_symbol('GIN')
        stock_exchange.remove_existing_stock_by_symbol('TEA')

    def test_add_new_trade(self):
        stock_exchange = StockExchange('test')
        stock = Stock('GIN', 'preferred', '8', '100', '2%', stock_exchange)
        stock_exchange.add_new_trade(TradeRecord(stock_exchange, 'GIN', '500', 'sell', '150', '2017-02-05 22:14:39'))
        stock_exchange.add_new_trade(TradeRecord(stock_exchange, 'GIN', '300', 'buy', '130', '2017-02-05 23:14:39'))
        stock_exchange.remove_existing_stock(stock)
        stock_exchange.add_new_trade(TradeRecord(stock_exchange, 'GIN', '200', 'sell', '150', '2017-02-05 23:15:39'))

    def test_remove_trade(self):
        stock_exchange = StockExchange('test')
        Stock('GIN', 'preferred', '8', '100', '2%', stock_exchange)
        trade = TradeRecord(stock_exchange, 'GIN', '300', 'buy', '130', '2017-02-05 23:14:39')
        trade1 = TradeRecord(stock_exchange, 'GIN', '500', 'sell', '150', '2017-02-05 22:14:39')
        stock_exchange.remove_trade(trade)
        stock_exchange.remove_trade(trade)
        stock_exchange.remove_trade(trade1)
        stock_exchange.remove_trade(trade1)

    def test_remove_trade_by_symbol_date(self):
        stock_exchange = StockExchange('test')
        Stock('GIN', 'preferred', '8', '100', '2%', stock_exchange)
        TradeRecord(stock_exchange, 'GIN', '300', 'buy', '130', '2017-02-05 23:14:39')
        TradeRecord(stock_exchange, 'GIN', '500', 'sell', '150', '2017-02-05 22:14:39')
        stock_exchange.remove_trade_by_symbol_date('GIN', '2017-02-05 23:14:39')
        stock_exchange.remove_trade_by_symbol_date('GIN', '2017-02-05 23:14:39')
        stock_exchange.remove_trade_by_symbol_date('GIN', '2017-02-05 22:14:39')
        stock_exchange.remove_trade_by_symbol_date('GIN', '2017-02-05 22:14:39')

    def test_is_stock_price_valid(self):
        StockExchange.is_stock_price_valid('400.35')
        StockExchange.is_stock_price_valid('test')
        StockExchange.is_stock_price_valid('0.0')

    def test_dividend_yield_calculator(self):
        stock_exchange = StockExchange('test')
        Stock('TEA', 'common', '0', '100', current_stock_exchange=stock_exchange)
        dividend = stock_exchange.dividend_yield_calculator('TEA', '200')
        self.assertEqual(dividend, 0.0)
        Stock('POP', 'common', '8', '100', current_stock_exchange=stock_exchange)
        dividend = stock_exchange.dividend_yield_calculator('POP', '150')
        self.assertEqual(dividend, 0.053)
        Stock('GIN', 'preferred', '8', '100', '2%', stock_exchange)
        dividend1 = stock_exchange.dividend_yield_calculator('GIN', '350')
        self.assertEqual(dividend1, 0.006)

    def test_p_e_ratio_calculator(self):
        stock_exchange = StockExchange('test')
        Stock('POP', 'common', '8', '100', current_stock_exchange=stock_exchange)
        stock_exchange.dividend_yield_calculator('POP', '150')
        p_e_ratio = stock_exchange.p_e_ratio_calculator('POP', '150')
        self.assertEqual(p_e_ratio, 18.75)
        p_e_ratio1 = stock_exchange.p_e_ratio_calculator('POP', '250')
        self.assertEqual(p_e_ratio1, 31.25)
        Stock('TEA', 'common', '0', '100', current_stock_exchange=stock_exchange)
        p_e_ratio2 = stock_exchange.p_e_ratio_calculator('TEA', '150')
        self.assertIsNone(p_e_ratio2)
        Stock('ALE', 'common', '23', '60', current_stock_exchange=stock_exchange)
        p_e_ratio3 = stock_exchange.p_e_ratio_calculator('ALE', '140')
        self.assertEqual(p_e_ratio3, 6.087)

    def test_all_share_index_calculator(self):
        stock_exchange = StockExchange('test')
        stock_exchange.all_share_index_calculator()
        stock = Stock('POP', 'common', '8', '100')
        stock.current_price = 150
        stock_exchange.add_new_stock(stock)
        stock1 = Stock('TEA', 'common', '0', '100')
        stock1.current_price = 250
        stock_exchange.add_new_stock(stock1)
        stock2 = Stock('GIN', 'preferred', '8', '100', '2%')
        stock_exchange.add_new_stock(stock2)
        all_share_index = stock_exchange.all_share_index_calculator()
        self.assertEqual(all_share_index, 155.362)

    def test_vw_stock_price_calculator(self):
        stock_exchange = StockExchange('test')
        Stock('GIN', 'preferred', '8', '100', '2%', stock_exchange)
        TradeRecord(stock_exchange, 'GIN', '300', 'buy', '130')
        TradeRecord(stock_exchange, 'GIN', '500', 'sell', '150')
        TradeRecord(stock_exchange, 'GIN', '200', 'sell', '120')
        stock_exchange.vw_stock_price_calculator('TEA')
        stock_exchange.vw_stock_price_calculator('GIN', '10')
        stock_exchange.vw_stock_price_calculator('GIN', 'test')
        volume_weighted_price = stock_exchange.vw_stock_price_calculator('GIN')
        self.assertEqual(volume_weighted_price, 138.0)

    def test_vw_stock_price_calculator1(self):
        stock_exchange = StockExchange('test')
        Stock('GIN', 'preferred', '8', '100', '2%', stock_exchange)
        TradeRecord(stock_exchange, 'GIN', '300', 'buy', '130', '2017-01-05 21:14:39')
        TradeRecord(stock_exchange, 'GIN', '500', 'sell', '150', '2017-01-05 22:14:39')
        TradeRecord(stock_exchange, 'GIN', '200', 'sell', '120', '2017-01-05 23:14:39')
        volume_weighted_price = stock_exchange.vw_stock_price_calculator('GIN')
        self.assertIsNone(volume_weighted_price)


        # with self.assertRaises(KeyError) as context:
        #     Stock('GIN', 'other', '8', '100', '0.02', stock_exchange)
        # print context.exception
        # self.assertTrue('This is broken' in context.exception)