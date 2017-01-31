
import logging
import sys
from enum import Enum
from stock_exchange import StockExchange
from datetime import datetime

__author__ = 'Nikitas Papangelopoulos'

logger = logging.getLogger(__name__)


class TradeRecord(object):
    # An enum to save the stock type.
    TradeType = Enum('TradeType', 'buy sell')

    def __init__(self, current_stock_exchange, stock_symbol, quantity, trade_type, traded_price, time_stamp=None):
        """
        The constructor, to create a new stock for the stock exchange.

        Args
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
        :return: the dividend yield value
        :rtype: float | None
        """
        logger.debug('Recording a new trade')
        # boolean to check if everything went OK.
        self.created_successfully = True

        # Assigning stock symbol.
        self.stock_symbol = stock_symbol

        # Assigning quantity of shares traded.
        try:
            self.quantity = int(quantity)
        except ValueError:
            logger.error('Quantity of shares must be a numerical value. You entered: {}'.format(quantity))
            self.created_successfully = False
            # sys.exit(1)
            # return False

        # Assigning trade type.
        try:
            self.trade_type = TradeRecord.TradeType[trade_type].name
        except KeyError:
            logger.error('Attempted to record a trade with invalid type: {}. Valid types are: {}'
                         .format(trade_type, TradeRecord.TradeType.__members__.keys()))#, exc_info=True)
            self.created_successfully = False
            # sys.exit(1)
            # return False

        # Assigning traded price of shares traded.
        try:
            self.traded_price = float(traded_price)
        except ValueError:
            logger.error('Traded price of shares must be a numerical value. You entered: {}'.format(traded_price))
            self.created_successfully = False
            # sys.exit(1)
            # return False

        # Assigning the timestamp.
        if time_stamp:
            # Attempting to convert the time to the appropriate format.
            try:
                self.time_stamp = datetime.strptime(time_stamp, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                logger.error('Timestamp provided must be in the following format "Y-m-d H:M:S". You entered: {}'.format(time_stamp))
                self.created_successfully = False
                # sys.exit(1)
                # return False
        else:
            self.time_stamp = datetime.strptime(str(datetime.now())[:-7], '%Y-%m-%d %H:%M:%S')

        # Assigning current_stock_exchange value.
        if isinstance(current_stock_exchange, StockExchange):
            self.current_stock_exchange = current_stock_exchange
        else:
            logger.error('Argument "current_stock_exchange" must be of type stock_exchange.StockExchange. You provided: {}'.format(current_stock_exchange))
            self.created_successfully = False

        if self.created_successfully:
            logger.info('Successfully created new trade with attributes stock_symbol: {}, quantity: {}, trade_type: {}, traded_price: {}, time_stamp: {}.'
                        .format(self.stock_symbol, self.quantity, self.trade_type, self.traded_price, self.time_stamp))
            self.current_stock_exchange.add_new_trade(self)
