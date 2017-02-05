#!/usr/bin/python

import logging

from enum import Enum

from stock_exchange import StockExchange

__author__ = 'Nikitas Papangelopoulos'

logger = logging.getLogger(__name__)


class Stock(object):
    """
    A class to model a stock that can be added in a StockExchange object.
    """
    # An enum to save the stock type.
    StockType = Enum('StockType', 'common preferred')

    def __init__(self, stock_symbol, stock_type, last_dividend, par_value, fixed_dividend=None,
                 current_stock_exchange=None):
        """
        The constructor, to create a new stock for the stock exchange.
        :param stock_symbol: the symbol (abbreviated name) of the stock
        :type stock_symbol: str
        :param stock_type: the type of the stock
        :type stock_type: Enum StockType: common | preferred
        :param last_dividend: the last dividend of the stock
        :type last_dividend: str
        :param par_value: the par value of the stock
        :type par_value: str
        :param fixed_dividend: the fixed dividend of the stock, if any (optional)
        :type fixed_dividend: str (default: None)
        :param current_stock_exchange: An optional StockExchange object, in which to register the stock.
        :type current_stock_exchange: StockExchange
        """
        logger.debug('Creating a new stock')
        # boolean to check if everything went OK.
        self.created_successfully = True

        # Assigning stock symbol.
        self.stock_symbol = stock_symbol

        # Assigning stock type.
        try:
            self.stock_type = Stock.StockType[stock_type].name
        except KeyError:
            logger.error('Attempted to add stock with invalid type: {}. Valid types are: {}'
                         .format(stock_type, Stock.StockType.__members__.keys()))  # , exc_info=True)
            self.created_successfully = False

        # Assigning last dividend.
        try:
            self.last_dividend = float(last_dividend)
        except ValueError:
            logger.error('Last dividend must be a numerical value. You entered: {}'.format(last_dividend))
            self.created_successfully = False

        # Assigning fixed dividend.
        try:
            if fixed_dividend:
                # Catering for percentage values
                if fixed_dividend[-1] is '%':
                    self.fixed_dividend = float(fixed_dividend[:-1]) / 100
                elif '.' not in fixed_dividend:
                    logger.error('Fixed dividend must be a percentage or decimal number value. You entered: {}'.format(
                        fixed_dividend))
                    self.created_successfully = False
                else:
                    self.fixed_dividend = float(fixed_dividend)
            else:
                self.fixed_dividend = fixed_dividend
        except ValueError:
            logger.error('Fixed dividend must be a numerical value. You entered: {}'.format(fixed_dividend))
            self.created_successfully = False

            # If the type is preferred, a fixed dividend must be always provided.
            if self.stock_type is 'preferred' and self.fixed_dividend is None:
                logger.error("You provided a 'preferred' stock type. You must also provided a fixed_dividend")
                self.created_successfully = False
                # sys.exit(1)

        # Assigning par value.
        try:
            self.par_value = float(par_value)
        except ValueError:
            logger.error('Par value must be a numerical value. You entered: {}'.format(par_value))
            self.created_successfully = False

        # Assigning current_stock_exchange value.
        if current_stock_exchange:
            if isinstance(current_stock_exchange, StockExchange):
                self.current_stock_exchange = current_stock_exchange
            else:
                logger.error(
                    'Argument "current_stock_exchange" must be of type stock_exchange.StockExchange. '
                    'You provided: {}'.format(current_stock_exchange))
                self.created_successfully = False

        # Initializing dividend_yield and P/E ratio.
        self.current_price = ''
        self.current_price_timestamp = ''
        self.dividend_yield = ''
        self.p_e_ratio = ''

        if self.created_successfully:
            logger.info(
                'Successfully created new stock with attributes stock_symbol: {},stock_type: {}, last_dividend: {}, '
                'fixed_dividend: {}, par_value: {}'.format(self.stock_symbol, self.stock_type, self.last_dividend,
                                                           self.fixed_dividend, self.par_value))
            # After creation, adding the stock to the stock exchange
            if current_stock_exchange:
                self.current_stock_exchange.add_new_stock(self)
