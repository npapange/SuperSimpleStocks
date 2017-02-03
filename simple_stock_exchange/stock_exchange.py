#!/usr/bin/python

import logging
import numpy as np
from datetime import datetime, timedelta

__author__ = 'Nikitas Papangelopoulos'

logger = logging.getLogger(__name__)
# Constant to use for time frame when calculating the volume weighted stock price.
MINUTES_FOR_VW_PRICE = 15


class StockExchange(object):

    def __init__(self, name):
        # Creating a new stock exchange:
        self.name = name
        self.registered_stocks = {}
        self.recorded_trades = {}
        self.all_share_index = ''
        logger.info('Successfully created new stock exchange with attributes name: {}.'.format(self.name))

    def add_new_trade(self, trade_to_add):
        # Checking if the stock is registered in the market before recording a trade.
        if self.is_stock_registered(trade_to_add.stock_symbol):

            # Updating the stock price and timestamp only if it is newer than the existing.
            self.update_stock_price(trade_to_add)

            try:
                self.recorded_trades[trade_to_add.stock_symbol].append(trade_to_add)
            except KeyError:
                self.recorded_trades[trade_to_add.stock_symbol] = [trade_to_add]
            logger.info('Recorded new trade: {}, in stock_exchange with timestamp {}.'.format(trade_to_add.stock_symbol, trade_to_add.time_stamp))
            return True
        else:
            logger.info('Then retry recording the trade.')
            return False

    def remove_trade(self, trade_to_remove):
        # Checking if trade of that symbol exist in the stock exchange.
        if self.recorded_trades[trade_to_remove.stock_symbol]:
            try:
                self.recorded_trades[trade_to_remove.stock_symbol].remove(trade_to_remove)
                # If no trades are left for the specific stock, remove the key:value completely.
                if len(self.recorded_trades[trade_to_remove.stock_symbol]) == 0:
                    self.recorded_trades.pop(trade_to_remove.stock_symbol)
                logger.info('Removed trade for stock: {}, from stock_exchange.'.format(trade_to_remove.stock_symbol))
                return True
            except ValueError:
                logger.warning('Could not remove trade. It was not found in the stock_exchange.')
                return False
        else:
            logger.warning('Could not remove trade. No trades in the stock_exchange for stock: {}.'.format(trade_to_remove.stock_symbol))
            return False

    def remove_trade_by_symbol_date(self, trade_stock_symbol, trade_timestamp):
        """
        A method to remove a specific trade from the exchange, by using the stock symbol and timestamp as unique
        identifiers. This requires that no two trades dor the same stock, happened at the same time. In the opposite
        case, it will remove only the first one.
        :param trade_stock_symbol: the symbol (abbreviated name) of the stock
        :type trade_stock_symbol: str
        :param trade_timestamp: the timestamp when the trade occurred.
        :type trade_stock_symbol: datetime
        :return: a boolean for whether the operation completed successfully.
        :rtype: bool
        """
        # Checking if trade of that symbol exist in the stock exchange.
        if self.recorded_trades[trade_stock_symbol]:
            # Using the date to match the trade for removal.
            matched_trades = [trade for trade in self.recorded_trades[trade_stock_symbol] if str(trade.time_stamp) == trade_timestamp]
            if matched_trades:
                self.remove_trade(matched_trades[0])
            else:
                logger.warning('Could not remove trade. No trades in the stock_exchange for stock: {} and timestamp.'.format(trade_stock_symbol, trade_timestamp))
            return False
        else:
            logger.warning('Could not remove trade. No trades in the stock_exchange for stock: {}.'.format(trade_stock_symbol))
            return False

    def add_new_stock(self, stock_to_add):
        # Checking if the stock is already registered.
        if not self.is_stock_registered(stock_to_add.stock_symbol, True):
            self.registered_stocks[stock_to_add.stock_symbol] = stock_to_add
            logger.info('Added new stock: {}, to stock_exchange'.format(stock_to_add.stock_symbol))
            return True
        else:
            logger.debug('Please remove it first.')
            return False

    def update_stock_price(self, trade_to_add):
        if self.registered_stocks[trade_to_add.stock_symbol].current_price_timestamp:
            if trade_to_add.time_stamp > self.registered_stocks[trade_to_add.stock_symbol].current_price_timestamp:
                self.registered_stocks[trade_to_add.stock_symbol].current_price = trade_to_add.traded_price
                self.registered_stocks[trade_to_add.stock_symbol].current_price_timestamp = trade_to_add.time_stamp
                logger.debug("Successfully updated stock price, for stock: {}. New price: {}".format(trade_to_add.stock_symbol, trade_to_add.traded_price))
                return True
        else:
            # Case when this is the first time a stock price is set.
            self.registered_stocks[trade_to_add.stock_symbol].current_price = trade_to_add.traded_price
            self.registered_stocks[trade_to_add.stock_symbol].current_price_timestamp = trade_to_add.time_stamp
            logger.debug("Successfully updated stock price, for stock: {}. New price: {}".format(trade_to_add.stock_symbol, trade_to_add.traded_price))
            return True
        return False

    def is_stock_registered(self, stock_symbol_to_check, adding_created_stock=False):
        if stock_symbol_to_check in self.registered_stocks.keys():
            logger.debug('Stock symbol: {}, has already been registered in the current stock exchange.'.format(stock_symbol_to_check))
            return True
        else:
            if not adding_created_stock:
                logger.warning('Stock symbol: {}, has not been registered yet in the current stock exchange. Please add it first'.format(stock_symbol_to_check))
            return False

    @staticmethod
    def is_stock_price_valid(price_to_check):
        try:
            stock_price = float(price_to_check)
            if stock_price != 0.0:
                return stock_price
            else:
                logger.error('Stock price must be a non zero numerical value. You entered: {}'.format(price_to_check))
        except ValueError:
            logger.error('Stock price must be a a non zero numerical value. You entered: {}'.format(price_to_check))
        return False

    def remove_existing_stock(self, stock_to_remove):
        if self.is_stock_registered(stock_to_remove.stock_symbol):
            self.registered_stocks.pop(stock_to_remove.stock_symbol)
            logger.info('Removed stock: {}, from stock_exchange'.format(stock_to_remove.stock_symbol))
            return True
        return False

    def remove_existing_stock_by_symbol(self, stock_symbol):
        if self.is_stock_registered(stock_symbol):
            self.registered_stocks.pop(stock_symbol)
            logger.info('Removed stock: {}, from stock_exchange'.format(stock_symbol))
            return True
        return False

    def dividend_yield_calculator(self, stock_symbol, stock_price):
        """
        A method to calculate the dividend yield of a stock, given its price.

        Args
        :param stock_symbol: the symbol (abbreviated name) of the stock
        :type stock_symbol: str
        :param stock_price: the price of the stock
        :type stock_price: str
        :return: the dividend yield value
        :rtype: float | None
        """
        dividend = None
        # Checking if the stock is registered in the stock exchange.
        if self.is_stock_registered(stock_symbol):
            current_stock = self.registered_stocks[stock_symbol]

            # Checking if the stock_price is valid
            validated_price = StockExchange.is_stock_price_valid(stock_price)
            if validated_price:
                # Updating the trade price and timestamp of the price for the stock
                current_stock.current_price = validated_price
                current_stock.current_price_timestamp = datetime.strptime(str(datetime.now())[:-7], '%Y-%m-%d %H:%M:%S')
                # Checking the type of the stock to use the correct equation.
                if current_stock.stock_type == 'common':
                    logger.debug('Calculating dividend yield, for common stock type.')
                    dividend = np.round(np.divide(current_stock.last_dividend, validated_price), decimals=2)

                elif current_stock.stock_type == 'preferred':
                    logger.debug('Calculating dividend yield, for preferred stock type.')
                    dividend = np.round(np.divide(np.multiply(current_stock.fixed_dividend, current_stock.par_value), validated_price), decimals=2)

                logger.info('Successfully calculated dividend yield: {}, for stock: {} and price: {}'.format(dividend, stock_symbol, stock_price))

        return dividend

    def p_e_ratio_calculator(self, stock_symbol, stock_price):
        """

        :rtype: object
        :param stock_price:
        :type stock_symbol: str
        """
        p_e_ratio = None
        # Checking if the stock is registered in the stock exchange.
        if self.is_stock_registered(stock_symbol):
            current_stock = self.registered_stocks[stock_symbol]

            # Checking if the stock_price is valid
            validated_price = StockExchange.is_stock_price_valid(stock_price)
            if validated_price:

                # Checking if the dividend yield has already been successfully calculated for the specific stock
                if current_stock.dividend_yield == '':
                    logger.debug('Dividend yield has not yet been calculated for stock: {}. Calculating...'.format(stock_symbol))
                    dividend = self.dividend_yield_calculator(stock_symbol, stock_price)
                else:
                    logger.debug('Dividend yield has been calculated for stock: {}. Retrieving...'.format(stock_symbol))
                    dividend = current_stock.dividend_yield

                # Catering for dividend = None. TODO: maybe end program before and remove try-except
                try:
                    p_e_ratio = np.round(np.divide(validated_price, dividend), decimals=2)
                    logger.info('Successfully calculated p_e_ratio: {}, for stock: {} and price: {}'.format(p_e_ratio, stock_symbol, stock_price))
                except TypeError as error:
                    logger.error('Tried to calculate p_e_ratio, but got error: {}'.format(error))

        return p_e_ratio

    def all_share_index_calculator(self):
        # Checking if there are any stocks in the stock exchange
        if self.registered_stocks:
            all_stock_prices = [self.registered_stocks[price_symbol].current_price if self.registered_stocks[price_symbol].current_price is not '' else self.registered_stocks[price_symbol].par_value for price_symbol in self.registered_stocks.keys()]
            return np.round(np.power(np.prod(all_stock_prices), np.divide(1, float(len(all_stock_prices)))), decimals=3)

        else:
            logger.warning('Stock exchange is empty. Please register some stocks first, record some trades and then retry.')
            return None

    def vw_stock_price_calculator(self, stock_symbol, time_span=None):
        volume_weighted_price = None
        if not time_span:
            time_span = MINUTES_FOR_VW_PRICE
        else:
            # In case of user provided time span, checking if it is a valid number
            try:
                time_span = int(time_span)
            except ValueError:
                logger.error('Time span must be a numerical value. You entered: {}'.format(time_span))
                return False

        starting_time = datetime.today() - timedelta(minutes=time_span)
        # Checking if the stock is registered in the stock exchange.
        if self.is_stock_registered(stock_symbol):
            # Collecting trades for this particular stock over the specified time frame.
            latest_trades = [trade for trade in self.recorded_trades[stock_symbol] if trade.time_stamp > starting_time]
            if latest_trades:
                # Getting the denominator. reduce/lambda is used only for knowledge demonstration purposes. sum() is simpler
                denominator = float(reduce(lambda x, y: x+y, [trade.quantity for trade in latest_trades]))
                # Calculating the volume weighted stock price.
                volume_weighted_price = sum([np.round(np.divide(np.multiply(trade.traded_price, trade.quantity), denominator), decimals=3) for trade in latest_trades])
                logger.info('Successfully calculated the volume weighted price {} for stock: {}'.format(volume_weighted_price, stock_symbol))
            else:
                logger.info('No trades found for stock: {} in the last: {} nimutes. Unable to calculate volume weighted price.'.format(stock_symbol, MINUTES_FOR_VW_PRICE))

        return volume_weighted_price
