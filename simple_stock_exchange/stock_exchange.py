#!/usr/bin/python

import logging
from datetime import datetime, timedelta

import numpy as np

__author__ = 'Nikitas Papangelopoulos'

logger = logging.getLogger(__name__)

# Constant to use for time frame when calculating the volume weighted stock price.
MINUTES_FOR_VW_PRICE = 15


class StockExchange(object):
    """
    A class to model a simple stock exchange. Can contain stocks and trades for these stocks.
    It also includes methods for calculating various metrics for the stocks and trades.
    """

    def __init__(self, name):
        # Creating a new stock exchange:
        """
        Constructor.
        :param name: The name to give to the stock exchange when creating it
        :type name: str
        """
        self.name = name
        self.registered_stocks = {}
        self.recorded_trades = {}
        self.all_share_index = ''
        logger.info('Successfully created new stock exchange with attributes name: {}.'.format(self.name))

    def add_new_stock(self, stock_to_add):
        """
        A method to add a stock to the stock exchange.
        :param stock_to_add: The stock object to add to the stock exchange
        :type stock_to_add: Stock
        :return: True || False, whether the stock was added successfully in the stock exchange.
        :rtype: bool
        """
        # Checking if the stock is already registered.
        if not self.is_stock_registered(stock_to_add.stock_symbol, True):
            self.registered_stocks[stock_to_add.stock_symbol] = stock_to_add
            logger.info('Added new stock: {}, to stock_exchange'.format(stock_to_add.stock_symbol))
            return True
        else:
            logger.debug('Please remove it first.')
            return False

    def remove_existing_stock(self, stock_to_remove):
        """
        A method to remove a stock from the stock exchange.
        :param stock_to_remove: The stock object to remove from the stock exchange
        :type stock_to_remove: Stock
        :return: True || False, whether the stock was removed successfully from the stock exchange.
        :rtype: bool
        """
        if self.is_stock_registered(stock_to_remove.stock_symbol):
            self.registered_stocks.pop(stock_to_remove.stock_symbol)
            logger.info('Removed stock: {}, from stock_exchange'.format(stock_to_remove.stock_symbol))
            return True
        return False

    def remove_existing_stock_by_symbol(self, stock_symbol):
        """
        A method to remove a stock from the stock exchange using its symbol as a unique identifier.
        :param stock_symbol: The symbol of the stock to remove from the stock exchange.
        :type stock_symbol: str
        :return: True || False, whether the stock was removed successfully from the stock exchange.
        :rtype: bool
        """
        if self.is_stock_registered(stock_symbol):
            self.registered_stocks.pop(stock_symbol)
            logger.info('Removed stock: {}, from stock_exchange'.format(stock_symbol))
            return True
        return False

    def add_new_trade(self, trade_to_add):
        """
        A method to record a trade for a specific stock to the stock exchange.
        :param trade_to_add: The trade object to add to the stock exchange
        :type trade_to_add: TradeRecord
        :return: True || False, whether the trade was recorded successfully in the stock exchange.
        :rtype: bool
        """
        # Checking if the stock is registered in the market before recording a trade.
        if self.is_stock_registered(trade_to_add.stock_symbol):

            # Updating the stock price and timestamp only if it is newer than the existing.
            self.update_stock_price(trade_to_add)

            if trade_to_add.stock_symbol in self.recorded_trades:
                self.recorded_trades[trade_to_add.stock_symbol].append(trade_to_add)
            else:
                self.recorded_trades[trade_to_add.stock_symbol] = [trade_to_add]
            logger.info('Recorded new trade: {}, in stock_exchange with timestamp {}.'.format(trade_to_add.stock_symbol,
                                                                                              trade_to_add.time_stamp))
            return True
        else:
            logger.info('Then retry recording the trade.')
            return False

    def remove_trade(self, trade_to_remove):
        """
        A method to remove a trade for a specific stock from the stock exchange.
        :param trade_to_remove: The trade object to remove from the stock exchange
        :type trade_to_remove: TradeRecord
        :return: True || False, whether the trade was removed successfully from the stock exchange.
        :rtype: bool
        """
        # Checking if trade of that symbol exist in the stock exchange.
        if trade_to_remove.stock_symbol in self.recorded_trades:
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
            logger.warning('Could not remove trade. No trades in the stock_exchange for stock: {}.'.format(
                trade_to_remove.stock_symbol))
            return False

    def remove_trade_by_symbol_date(self, trade_stock_symbol, trade_timestamp):
        """
        A method to remove a specific trade from the exchange, by using the stock symbol and timestamp as unique
        identifiers. This requires that no two trades for the same stock, happened at the same time. In the opposite
        case, it will remove only the first one.
        :param trade_stock_symbol: the symbol (abbreviated name) of the stock.
        :type trade_stock_symbol: str
        :param trade_timestamp: the timestamp when the trade occurred.
        :type trade_timestamp: str
        :return: True || False, whether the trade was removed successfully from the stock exchange.
        :rtype: bool
        """
        # Checking if trade of that symbol exist in the stock exchange.
        if trade_stock_symbol in self.recorded_trades:
            # Using the date to match the trade for removal.
            matched_trades = [trade for trade in self.recorded_trades[trade_stock_symbol] if
                              str(trade.time_stamp) == trade_timestamp]
            if matched_trades:
                self.remove_trade(matched_trades[0])
                return True
            else:
                logger.warning(
                    'Could not remove trade. No trades in the stock_exchange for stock: {} and timestamp.'.format(
                        trade_stock_symbol, trade_timestamp))
            return False
        else:
            logger.warning(
                'Could not remove trade. No trades in the stock_exchange for stock: {}.'.format(trade_stock_symbol))
            return False

    def update_stock_price(self, trade_to_add):
        """
        A helper method to assign or update the price of a stock each time a trade is recorded.
        The price will be updated only if the trade being added has a more recent price than the existing one.
        :param trade_to_add: The trade object that is being recorded. It is used to get the stock price
        :type trade_to_add: TradeRecord
        :return: True || False, whether the stock price was successfully assigned to the stock.
        :rtype: bool
        """
        # Checking if a price has already been set.
        if self.registered_stocks[trade_to_add.stock_symbol].current_price_timestamp:
            if trade_to_add.time_stamp > self.registered_stocks[trade_to_add.stock_symbol].current_price_timestamp:
                # Only updating the price if it is more recent than the existing one
                self.registered_stocks[trade_to_add.stock_symbol].current_price = trade_to_add.traded_price
                self.registered_stocks[trade_to_add.stock_symbol].current_price_timestamp = trade_to_add.time_stamp
                logger.debug(
                    "Successfully updated stock price, for stock: {}. New price: {}".format(trade_to_add.stock_symbol,
                                                                                            trade_to_add.traded_price))
                return True
        else:
            # Case when this is the first time a stock price is set.
            self.registered_stocks[trade_to_add.stock_symbol].current_price = trade_to_add.traded_price
            self.registered_stocks[trade_to_add.stock_symbol].current_price_timestamp = trade_to_add.time_stamp
            logger.debug(
                "Successfully updated stock price, for stock: {}. New price: {}".format(trade_to_add.stock_symbol,
                                                                                        trade_to_add.traded_price))
            return True
        return False

    def is_stock_registered(self, stock_symbol_to_check, adding_created_stock=False):
        """
        A helper method to check if a stock is already in the stock exchange.
        :param stock_symbol_to_check: the symbol (abbreviated name) of the stock.
        :type stock_symbol_to_check: str
        :param adding_created_stock: A boolean to avoid writing the second the log statement,
                                     when it is call from add_new_stock()
        :type adding_created_stock: bool
        :return: True || False, whether the stock price is registered or not.
        :rtype: bool
        """
        if stock_symbol_to_check in self.registered_stocks.keys():
            logger.debug('Stock symbol: {}, has already been registered in the current stock exchange.'.format(
                stock_symbol_to_check))
            return True
        else:
            if not adding_created_stock:
                logger.warning('Stock symbol: {}, has not been registered yet in the current stock exchange. '
                               'Please add it first'.format(stock_symbol_to_check))
            return False

    @staticmethod
    def is_stock_price_valid(price_to_check):
        """
        A helper method to check if a user provided stock can be converted to float.
        :param price_to_check: The price of the stock to check.
        :type price_to_check:: str
        :return: True || False, whether the stock price is valid or not.
        :rtype: bool
        """
        try:
            stock_price = float(price_to_check)
            if stock_price != 0.0:
                return stock_price
            else:
                logger.error('Stock price must be a non zero numerical value. You entered: {}'.format(price_to_check))
        except ValueError:
            logger.error('Stock price must be a a non zero numerical value. You entered: {}'.format(price_to_check))
        return False

    def dividend_yield_calculator(self, stock_symbol, stock_price):
        """
        A method to calculate the dividend yield of a stock, given its price.
        :param stock_symbol: the symbol (abbreviated name) of the stock
        :type stock_symbol: str
        :param stock_price: the price of the stock
        :type stock_price: str
        :return: the dividend yield value or None, if for some reason the calculation failed.
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
                    dividend = np.round(np.divide(current_stock.last_dividend, validated_price), decimals=3)
                elif current_stock.stock_type == 'preferred':
                    logger.debug('Calculating dividend yield, for preferred stock type.')
                    dividend = np.round(
                        np.divide(np.multiply(current_stock.fixed_dividend, current_stock.par_value), validated_price),
                        decimals=3)
                logger.info('Successfully calculated dividend yield: {}, for stock: {} and price: {}'
                            .format(dividend, stock_symbol, stock_price))
                current_stock.dividend_yield = dividend
        return dividend

    def p_e_ratio_calculator(self, stock_symbol, stock_price):
        """
        A method to calculate the P/E ratio of a stock, given its price.
        :param stock_symbol: the symbol (abbreviated name) of the stock
        :type stock_symbol: str
        :param stock_price: the price of the stock
        :type stock_price: str
        :return: the P/E ratio value or None, if for some reason the calculation failed.
        :rtype: float | None
        """
        p_e_ratio = None
        # Checking if the stock is registered in the stock exchange.
        if self.is_stock_registered(stock_symbol):
            current_stock = self.registered_stocks[stock_symbol]

            # Checking if the stock_price is valid
            validated_price = StockExchange.is_stock_price_valid(stock_price)
            if validated_price:
                denominator = 0.0
                # Checking the type of the stock to use the correct equation.
                if current_stock.stock_type == 'common':
                    logger.debug('Calculating dividend, for common stock type.')
                    denominator = current_stock.last_dividend
                elif current_stock.stock_type == 'preferred':
                    logger.debug('Calculating dividend, for preferred stock type.')
                    denominator = np.multiply(current_stock.fixed_dividend, current_stock.par_value)

                try:
                    # Post process to avoid division by zero.
                    if denominator != 0.0:
                        p_e_ratio = np.round(np.divide(validated_price, denominator), decimals=3)
                        logger.info('Successfully calculated P/E ratio: {}, for stock: {} '
                                    'and price: {}'.format(p_e_ratio, stock_symbol, stock_price))
                except TypeError as error:
                    logger.error('Tried to calculate P/E ratio, but got error: {}'.format(error))

        return p_e_ratio

    def all_share_index_calculator(self):
        """
        A method to calculate the all share index for all stocks in the stock exchange.
        :return: the all share index value or None, if for some reason the calculation failed.
        :rtype: float | None
        """
        # Checking if there are any stocks in the stock exchange
        if self.registered_stocks:
            all_stock_prices = [self.registered_stocks[price_symbol].current_price
                                if self.registered_stocks[price_symbol].current_price is not ''
                                else self.registered_stocks[price_symbol].par_value for price_symbol in
                                self.registered_stocks.keys()]
            all_share_index = np.round(np.power(np.prod(all_stock_prices), np.divide(1, float(len(all_stock_prices)))),
                                       decimals=3)
            logger.info('Successfully calculated the all share index: {}'.format(all_share_index))
            return all_share_index

        else:
            logger.warning(
                'Stock exchange is empty. Please register some stocks first, record some trades and then retry.')
            return None

    def vw_stock_price_calculator(self, stock_symbol, time_span=None):
        """
        A method to calculate the volume weighted price of a stock, for a given time frame.
        :param stock_symbol: the symbol (abbreviated name) of the stock
        :type stock_symbol: str
        :param time_span: A user provided time span in minutes
        :type time_span: str
        :return: the volume weighted price value or None, if for some reason the calculation failed.
        :rtype: float | None
        """
        volume_weighted_price = None
        # Setting the default time span, if the user didn't provide any.
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
                # Getting the denominator. reduce/lambda is used only for
                # knowledge demonstration purposes. sum() is simpler
                denominator = float(reduce(lambda x, y: x + y, [trade.quantity for trade in latest_trades]))
                # Calculating the volume weighted stock price.
                volume_weighted_price = sum(
                    [np.round(np.divide(np.multiply(trade.traded_price, trade.quantity), denominator), decimals=3) for
                     trade in latest_trades])
                logger.info(
                    'Successfully calculated the volume weighted price {} for stock: {}'.format(volume_weighted_price,
                                                                                                stock_symbol))
            else:
                logger.info('No trades found for stock: {} in the last: {} minutes. '
                            'Unable to calculate volume weighted price.'.format(stock_symbol, MINUTES_FOR_VW_PRICE))

        return volume_weighted_price
