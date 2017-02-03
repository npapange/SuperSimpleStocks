#!/usr/bin/python

import argparse
import logging.config
import sys
from simple_stock_exchange import Stock, TradeRecord, StockExchange


__author__ = 'Nikitas Papangelopoulos'

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

stock_exchange = None


def main(use_method):
    """
    A method to take the user's input and decide which method to call
    :param use_method: The method teh user wants to use.
    :type use_method: str
    """
    # Converting the user's request to actual method to call.
    choose_method(use_method)


def choose_method(use_method):
    """
    A 'switch-case' method to convert the user's request to method to run
    :param use_method: The name of the method asked by the user
    :type: str
    :return: The python method to use
    :rtype: object
    """
    return {
        'create_exchange_market': create_exchange_market,
        'create_stock': create_stock,
        'add_stock': add_stock,
        'remove_stock': remove_stock,
        'add_trade': add_trade,
        'remove_trade': remove_trade,
        'calculate_dividend': calculate_dividend,
        'calculate_p_e_ratio': calculate_p_e_ratio,
        'calculate_volume_weighted_price': calculate_volume_weighted_price,
        'calculate_all_share_index': calculate_all_share_index,
    }.get(use_method)()


def create_exchange_market():
    """
    A console wrapper for StockExchange
    :return: Recursion
    """
    global stock_exchange
    if not stock_exchange:
        user_provided_args = raw_input('Please provide an exchange market name, or \'q\'to quit\n:')
        exit_program(user_provided_args)
        try:
            stock_exchange = StockExchange(user_provided_args.strip())
        except TypeError as error:
            print error
        # Retrying
        return create_exchange_market()


def create_stock(from_=''):
    """
    A console wrapper for Stock
    :param from_: An optional argument for keeping track which method called add_stock()
    :return: Recursion || calculate_p_e_ratio() || calculate_dividend
    """
    user_provided_args = raw_input(
        'Please provide stock information in the following format:\nstock symbol, stock type, last dividend, '
        'par value, fixed dividend (if any), or \'q\'to quit\n:')
    exit_program(user_provided_args)
    user_provided_args = [arg.strip() for arg in user_provided_args.split(',') if arg]

    try:
        created_stock = ''
        # Stock can be created either with fixed dividend or not.
        if len(user_provided_args) < 5:
            created_stock = Stock(user_provided_args[0], user_provided_args[1], user_provided_args[2],
                                  user_provided_args[3])
        elif len(user_provided_args) == 5:
            created_stock = Stock(user_provided_args[0], user_provided_args[1], user_provided_args[2],
                                  user_provided_args[3], user_provided_args[4])
    except TypeError as error:
        print error
        # Retrying
        return create_stock(from_='')

    if not from_:
        # Normal case when method was create_stock. Recursion so that the user can create many stocks.
        return create_stock(from_)
    else:
        # Case when create_stock is called from calculate_p_e_ratio. Sending the created stock back.
        if from_ == 'calculate_p_e_ratio':
            return calculate_p_e_ratio(created_stock)
        else:
            # Case when create_stock is called from calculate_dividend. Sending the created stock back.
            return calculate_dividend(created_stock)


def add_stock(from_=''):
    """
    A console wrapper for StockExchange.add_stock
    :param from_: An optional argument for keeping track which method called add_stock()
    :return: Recursion
    """
    # Creating a stock exchange (if one does not already exists) to register the created stocks.
    create_exchange_market()

    user_provided_args = ''
    user_prompt = 'Please provide stock for addition information in the following format:\nstock symbol, stock type, ' \
                  'last dividend, par value, fixed dividend (if any),'
    # Normal case. User asked for add_stock()
    if not from_:
        user_provided_args = raw_input(user_prompt + ' or \'q\'to quit\n:')
    # Case when add_stock() is called from add_trade() -> add_stock() -> add_trade()
    elif from_ == 'add_trade':
        user_provided_args = raw_input(user_prompt + '\n"trade" to start adding trades or \'q\'to quit\n:')
        if user_provided_args.strip() == 'trade':
            add_trade()
    # Case when add_stock() is called from remove_trade() -> add_trade() -> add_stock() -> add_trade()
    elif from_ == 'remove_trade':
        user_provided_args = raw_input(user_prompt + '\n"trade" to start adding trades or \'q\'to quit\n:')
        if user_provided_args.strip() == 'trade':
            add_trade('remove_trade')
    # Case when add_stock() is called from calculate_volume_weighted_price() -> add_trade() -> add_stock() ->add_trade()
    elif from_ == 'volume_weighted_price':
        user_provided_args = raw_input(user_prompt + '\n"trade" to start adding trades or \'q\'to quit\n:')
        if user_provided_args.strip() == 'trade':
            add_trade('volume_weighted_price')
    # Case when add_stock() is called from calculate_all_share_index() -> add_trade() -> add_stock()-> add_trade()
    elif from_ == 'all_share_index':
        user_provided_args = raw_input(user_prompt + '\n"trade" to start adding trades or \'q\'to quit\n:')
        if user_provided_args.strip() == 'trade':
            add_trade('all_share_index')
    # Case when add_stock() is called from remove_stock() -> add_stock() -> remove_stock()
    elif from_ == 'remove_stock':
        user_provided_args = raw_input(user_prompt + '\n"remove" to start removing stocks or \'q\'to quit\n:')
        if user_provided_args.strip() == 'remove':
            remove_stock()
    exit_program(user_provided_args)

    user_provided_args = [arg.strip() for arg in user_provided_args.split(',') if arg]
    # Stock can be created either with fixed dividend or not.
    try:
        if len(user_provided_args) < 5:
            Stock(user_provided_args[0], user_provided_args[1], user_provided_args[2], user_provided_args[3],
                  current_stock_exchange=stock_exchange)
        elif len(user_provided_args) == 5:
            Stock(user_provided_args[0], user_provided_args[1], user_provided_args[2], user_provided_args[3],
                  user_provided_args[4], stock_exchange)
        # Recursion to add more stocks
        return add_stock(from_)
    except TypeError as error:
        print error
        # Retrying
        return add_stock(from_)


def remove_stock():
    """
    A console wrapper for StockExchange.remove_existing_stock_by_symbol
    :return: Recursion
    """
    global stock_exchange
    # Calling add_stock(), only in the first run, to add new stocks that can be later removed.
    if not stock_exchange:
        add_stock('remove_stock')
    else:
        user_provided_args = raw_input(
            'Please provide stock for removal information in the following format:\nstock symbol, or \'q\'to quit\n:')
        exit_program(user_provided_args)
        try:
            stock_exchange.remove_existing_stock_by_symbol(user_provided_args.strip())
        except TypeError as error:
            print error
            # Retrying
            return remove_stock()

    # Recursion to remove more stocks, while there are still remaining.
    while stock_exchange.registered_stocks:
        return remove_stock()
    print 'No more stocks to remove'
    sys.exit(0)


def add_trade(from_='add_trade'):
    """
    A console wrapper for TradeRecord
    :param from_: An optional argument for keeping track which method called add_trade()
    :return: Recursion or add_stock()
    """
    create_exchange_market()

    user_provided_args = ''
    if stock_exchange.registered_stocks:
        user_prompt = 'Please provide trade information for addition in the following format:\nstock symbol, ' \
                      'quantity, trade type, traded price, time stamp (Y-m-d H:M:S or empty to use current time.), '
        # Normal case. User Asked for add_trade().
        if from_ == 'add_trade':
            user_provided_args = raw_input(user_prompt + ' or \'q\'to quit\n:')
        # Case when add_trade() is called from remove_trade() -> add_trade()-> add_stock()-> add_trade()->remove_trade()
        elif from_ == 'remove_trade':
            user_provided_args = raw_input(user_prompt + '\n"remove" to start removing trades or \'q\'to quit\n:')
            if user_provided_args.strip() == 'remove':
                remove_trade()
        # Case when add_trade() is called from calculate_volume_weighted_price()-> add_trade()-> add_stock()->
        # add_trade()-> calculate_volume_weighted_price()
        elif from_ == 'volume_weighted_price':
            user_provided_args = raw_input(
                user_prompt + '\n"vw" to calculate the volume weighted price or \'q\'to quit\n:')
            if user_provided_args.strip() == 'vw':
                calculate_volume_weighted_price()
        # Case when add_trade() is called from calculate_all_share_index() -> add_trade() -> add_stock()-> add_trade()
        # -> calculate_all_share_index()
        elif from_ == 'all_share_index':
            user_provided_args = raw_input(
                user_prompt + '\n"index" to calculate all share index or \'q\'to quit\n:')
            if user_provided_args.strip() == 'index':
                calculate_volume_weighted_price()
        exit_program(user_provided_args)

        user_provided_args = [arg.strip() for arg in user_provided_args.split(',') if arg]

        # Checking if the trade the user wants to add is about an already registered stock.
        if stock_exchange.is_stock_registered(user_provided_args[0]):
            # TradeRecord can be created either with user provided or system provided timestamp.
            try:
                if len(user_provided_args) < 5:
                    TradeRecord(stock_exchange, user_provided_args[0], user_provided_args[1], user_provided_args[2],
                                user_provided_args[3])
                elif len(user_provided_args) == 5:
                    TradeRecord(stock_exchange, user_provided_args[0], user_provided_args[1], user_provided_args[2],
                                user_provided_args[3], user_provided_args[4])
            except TypeError as error:
                print error
                # Retrying
                return add_trade(from_)

            # Recursion to add more trades.
            return add_trade(from_)
        # The trade the user wants to add is about a non existing stock. prompting the user to add it.
        else:
            add_stock('add_trade')
    # First time running add_trade(). Need to first add stocks.
    else:
        print 'Stock Exchange Empty. Please register some stocks first.'
        add_stock(from_)


def remove_trade():
    """
    A console wrapper for StockExchange.remove_trade_by_symbol_date
    :return: Recursion
    """
    global stock_exchange
    # Calling add_trade(), only in the first run, to add new trades that can be later removed.
    # remove_trade()-> add_trade() -> add_stock() -> add_trade() -> remove_trade()
    try:
        if not stock_exchange:
            add_trade('remove_trade')
        else:
            user_provided_args = raw_input(
                'Please provide trade for removal information in the following format:\nstock symbol,'
                'time stamp (Y-m-d H:M:S) or \'q\'to quit\n:')
            exit_program(user_provided_args)

            user_provided_args = [arg.strip() for arg in user_provided_args.split(',') if arg]
            try:
                stock_exchange.remove_trade_by_symbol_date(user_provided_args[0], user_provided_args[1])
            except TypeError as error:
                print error
                # Retrying
                remove_trade()

        # Recursion to remove more trades, while there are still remaining.
        while stock_exchange.recorded_trades:
            return remove_trade()
        print 'No more trades to remove'
        sys.exit(0)
    except TypeError as error:
        print error
        # Retrying
        return remove_trade()


def calculate_dividend(created_stock=None):
    """
    A console wrapper for StockExchange.dividend_yield_calculator
    :param created_stock: an optional argument for a stock object, for when the method is called from create_stock.
    :type created_stock: Stock
    """
    global stock_exchange
    # Creating a stock exchange, on the first run, to register the stock and access dividend_yield_calculator()
    # Calling create_stock() to create the stock for which the dividend will be calculated. Only one stock is needed.
    try:
        if not stock_exchange:
            stock_exchange = StockExchange('temp')
            create_stock('calculate_dividend')
        else:
            user_provided_args = raw_input(
                'Please provide the price for stock: {}, or \'q\'to quit\n:'.format(created_stock.stock_symbol))
            exit_program(user_provided_args)
            stock_exchange.add_new_stock(created_stock)
            dividend = stock_exchange.dividend_yield_calculator(created_stock.stock_symbol, user_provided_args.strip())
            print 'Dividend yield for stock: {} and price: {} is: {}'.format(created_stock.stock_symbol,
                                                                             user_provided_args.strip(), dividend)
    except TypeError as error:
        print error
        # Retrying
        return calculate_dividend()


def calculate_p_e_ratio(created_stock=None):
    """
    A console wrapper for StockExchange.p_e_ratio_calculator
    :param created_stock: an optional argument for a stock object, for when the method is called from create_stock.
    :type created_stock: Stock
    """
    global stock_exchange
    # Creating a stock exchange, on the first run, to register the stock and access p_e_ratio_calculator()
    # Calling create_stock() to create the stock for which the p/e ratio will be calculated. Only one stock is needed.
    try:
        if not stock_exchange:
            stock_exchange = StockExchange('temp')
            create_stock('calculate_p_e_ratio')
        else:
            user_provided_args = raw_input(
                'Please provide the price for stock: {}, or \'q\'to quit\n:'.format(created_stock.stock_symbol))
            exit_program(user_provided_args)
            stock_exchange.add_new_stock(created_stock)
            p_e_ratio = stock_exchange.p_e_ratio_calculator(created_stock.stock_symbol, user_provided_args.strip())
            print 'P/E ratio for stock: {} and price: {} is: {}'.format(created_stock.stock_symbol,
                                                                        user_provided_args.strip(), p_e_ratio)
    except TypeError as error:
        print error
        # Retrying
        return calculate_p_e_ratio()


def calculate_volume_weighted_price():
    """
    A console wrapper for StockExchange.vw_stock_price_calculator
    """
    global stock_exchange
    # Creating a stock exchange, on the first run, to registers stocks and trades and access vw_stock_price_calculator()
    # Calling add_trade() to create stock(s) and related trades for which the p/e ratio will be calculated.

    if not stock_exchange:
        add_trade('volume_weighted_price')
    else:
        user_provided_args = raw_input(
            'Please provide the stock for which to calculate the volume weighted price in the following format:'
            '\nstock symbol, time span (optional, in minutes), or \'q\'to quit\n:')
        exit_program(user_provided_args)

        user_provided_args = [arg.strip() for arg in user_provided_args.split(',') if arg]
        # vw_stock_price_calculator() can be called with 1 or 2 arguments (default 15 minutes time span or user defined)
        try:
            if len(user_provided_args) < 2:
                stock_exchange.vw_stock_price_calculator(user_provided_args[0])
            elif len(user_provided_args) == 2:
                stock_exchange.vw_stock_price_calculator(user_provided_args[0], user_provided_args[1])
        except TypeError as error:
            print error
            # Retrying
            return calculate_volume_weighted_price()

    # recursion to calculate again some stock's volume weighted price
    return calculate_volume_weighted_price()


def calculate_all_share_index():
    """
    A console wrapper for StockExchange.all_share_index_calculator
    """
    global stock_exchange
    # Creating a stock exchange, on the first run, to registers stocks/trades and access all_share_index_calculator()
    # Calling add_trade() to create stock(s) and related trades for which the all share index will be calculated.
    # Stock prices are automatically updated when calling add_new_trade.
    if not stock_exchange:
        add_trade('all_share_index')
    else:
        try:
            all_share_index = stock_exchange.all_share_index_calculator()
            print 'All Share Index for stock exchange: {}, is: {}'.format(stock_exchange.name, all_share_index)
            sys.exit(0)
        except TypeError as error:
            print error
            # Retrying
            return calculate_all_share_index()


def exit_program(user_input):
    """
    Checks if user wants to quit
    :param user_input: If user input is 'q' or just '' (pressed enter) the program exits.
    :type user_input: str
    """
    if user_input in ['q', '']:
        print 'Exiting the program'
        sys.exit(0)


if __name__ == '__main__':
    # Getting the user's input.
    parser = argparse.ArgumentParser(
        description='A to sort a csv file based on a column and save the result to an output csv file')
    parser.add_argument('-m', '--use-method',
                        choices=['create_exchange_market', 'create_stock', 'add_stock', 'remove_stock', 'add_trade',
                                 'remove_trade', 'calculate_dividend', 'calculate_p_e_ratio',
                                 'calculate_volume_weighted_price', 'calculate_all_share_index'], required=True,
                        help='Choose the method that you would like to run')
    args = parser.parse_args()

    main(args.use_method)
    main('calculate_all_share_index')
