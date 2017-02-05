#!/usr/bin/python

import logging
from datetime import datetime

from enum import Enum

from stock_exchange import StockExchange

__author__ = 'Nikitas Papangelopoulos'

logger = logging.getLogger(__name__)


class TradeRecord(object):
    """
    A class to model a trade for a specific stock that can be added in a StockExchange object.
    """

    # An enum to save the stock type.
    TradeType = Enum('TradeType', 'buy sell')

    def __init__(self, current_stock_exchange, stock_symbol, quantity, trade_type, traded_price, time_stamp=None):
        """
        The constructor, to create a new trade for some stock in the stock exchange.
        Example Usage: trade = TradeRecord(StockExchange('example'), 'TEA', '500', 'sell', '150', '2017-02-05 22:14:39')
        :param current_stock_exchange: An optional StockExchange object, in which to register the stock.
        :type current_stock_exchange: StockExchange
        :param stock_symbol: the symbol (abbreviated name) of the stock
        :type stock_symbol: str
        :param quantity: The number of stocks traded.
        :type quantity: str
        :param trade_type: the type of the trade, buy or cell.
        :type trade_type: Enum TradeType: buy | sell
        :param traded_price: the price of the stock for this trade.
        :type traded_price: str
        :param time_stamp: the time stamp of the trade in the format: Y-m-d H:M:S. If none is provided .now() is used.
        :type time_stamp: str
        """
        logger.debug('Recording a new trade')
        # boolean to check if everything went OK.
        self.created_successfully = True

        # Assigning stock symbol.
        self.stock_symbol = stock_symbol

        # Assigning quantity of shares traded.
        # Using isdigit() instead of try/catch for knowledge demonstration purposes.
        if quantity.isdigit():
            self.quantity = int(quantity)
        else:
            logger.error('Quantity of shares must be a numerical value. You entered: {}'.format(quantity))
            self.created_successfully = False

        # Assigning trade type.
        try:
            self.trade_type = TradeRecord.TradeType[trade_type].name
        except KeyError:
            logger.error('Attempted to record a trade with invalid type: {}. Valid types are: {}'
                         .format(trade_type, TradeRecord.TradeType.__members__.keys()))
            self.created_successfully = False

        # Assigning traded price of shares traded.
        try:
            self.traded_price = float(traded_price)
        except ValueError:
            logger.error('Traded price of shares must be a numerical value. You entered: {}'.format(traded_price))
            self.created_successfully = False

        # Assigning the timestamp.
        if time_stamp:
            # Attempting to convert the time to the appropriate format.
            try:
                self.time_stamp = datetime.strptime(time_stamp, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                logger.error('Timestamp provided must be in the following format "Y-m-d H:M:S". '
                             'You entered: {}'.format(time_stamp))
                self.created_successfully = False
        else:
            self.time_stamp = datetime.strptime(str(datetime.now())[:-7], '%Y-%m-%d %H:%M:%S')

        # Assigning current_stock_exchange value.
        if isinstance(current_stock_exchange, StockExchange):
            self.current_stock_exchange = current_stock_exchange
        else:
            logger.error(
                'Argument "current_stock_exchange" must be of type stock_exchange.StockExchange. '
                'You provided: {}'.format(current_stock_exchange))
            self.created_successfully = False

        if self.created_successfully:
            logger.info(
                'Successfully created new trade with attributes stock_symbol: {}, quantity: {}, trade_type: {}, '
                'traded_price: {}, time_stamp: {}.'.format(self.stock_symbol, self.quantity, self.trade_type,
                                                           self.traded_price, self.time_stamp))
            self.current_stock_exchange.add_new_trade(self)
