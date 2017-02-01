import logging.config
import sys

from stock_exchange import StockExchange
from stock import Stock
from trade_record import TradeRecord

__author__ = 'Nikitas Papangelopoulos'

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

market_exchange = None


def main(use_method):
    match_method(use_method)


def match_method(use_method):
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
    global market_exchange
    if not market_exchange:
        user_provided_args = raw_input('Please provide an exchange market name, or \'q\'to quit\n:')
        exit_program(user_provided_args)
        market_exchange = StockExchange(user_provided_args.strip())


def create_stock(from_=''):
    user_provided_args = raw_input(
        'Please provide stock information in the following format:\nstock symbol, stock type, last dividend, par value, fixed dividend (if any), or \'q\'to quit\n:')
    exit_program(user_provided_args)
    user_provided_args = [arg.strip() for arg in user_provided_args.split(',') if arg]

    created_stock = ''
    if len(user_provided_args) < 5:
        created_stock = Stock(user_provided_args[0], user_provided_args[1], user_provided_args[2], user_provided_args[3])
    elif len(user_provided_args) == 5:
        created_stock = Stock(user_provided_args[0], user_provided_args[1], user_provided_args[2], user_provided_args[3], user_provided_args[4])

    if not from_:
        return create_stock(from_)
    else:
        # Case when create_stock is called from calculate_p_e_ratio.
        if from_ == 'calculate_p_e_ratio':
            return calculate_p_e_ratio(created_stock)
        else:
            # Case when create_stock is called from calculate_dividend.
            return calculate_dividend(created_stock)


def add_stock(from_=''):
    create_exchange_market()

    user_provided_args = ''
    user_prompt='Please provide stock for addition information in the following format:\nstock symbol, stock type, last dividend, par value, fixed dividend (if any),'
    if not from_:
        user_provided_args = raw_input(user_prompt + ' or \'q\'to quit\n:')
    elif from_ == 'add_trade':
        user_provided_args = raw_input(user_prompt + '\n"trade" to start adding trades or \'q\'to quit\n:')
        if user_provided_args.strip() == 'trade':
            add_trade()

    elif from_ == 'remove_trade':
        user_provided_args = raw_input(user_prompt + '\n"trade" to start adding trades or \'q\'to quit\n:')
        if user_provided_args.strip() == 'trade':
            add_trade('remove_trade')

    elif from_ == 'volume_weighted_price':
        user_provided_args = raw_input(user_prompt + '\n"trade" to start adding trades or \'q\'to quit\n:')
        if user_provided_args.strip() == 'trade':
            add_trade('volume_weighted_price')

    elif from_ == 'all_share_index':
        user_provided_args = raw_input(user_prompt + '\n"index" to calculate all_share_index or \'q\'to quit\n:')
        if user_provided_args.strip() == 'index':
            calculate_all_share_index()

    elif from_ == 'remove_stock':
        user_provided_args = raw_input(user_prompt + '\n"remove" to start removing stocks or \'q\'to quit\n:')
        if user_provided_args.strip() == 'remove':
            remove_stock()
    exit_program(user_provided_args)

    user_provided_args = [arg.strip() for arg in user_provided_args.split(',') if arg]
    if len(user_provided_args) < 5:
        Stock(user_provided_args[0], user_provided_args[1], user_provided_args[2], user_provided_args[3], current_stock_exchange=market_exchange)
    elif len(user_provided_args) == 5:
        Stock(user_provided_args[0], user_provided_args[1], user_provided_args[2], user_provided_args[3], user_provided_args[4], market_exchange)

    return add_stock(from_)


def remove_stock():
    global market_exchange

    if not market_exchange:
        add_stock('remove_stock')
    else:
        user_provided_args = raw_input(
            'Please provide stock for removal information in the following format:\nstock symbol, or \'q\'to quit\n:')
        exit_program(user_provided_args)
        market_exchange.remove_existing_stock(market_exchange.registered_stocks[user_provided_args.strip()])

    while market_exchange.registered_stocks:
        return remove_stock()
    print 'No more stocks to remove'
    sys.exit(0)


def add_trade(from_=''):
    create_exchange_market()
    user_provided_args = ''

    if market_exchange.registered_stocks:
        user_prompt='Please provide trade information for addition in the following format:\nstock symbol, quantity, trade type, traded price, time stamp (Y-m-d H:M:S or empty to use current time.), '
        if not from_:
            user_provided_args = raw_input(user_prompt + ' or \'q\'to quit\n:')
        elif from_ == 'remove_trade':
            user_provided_args = raw_input(user_prompt + '\n"remove" to start removing trades or \'q\'to quit\n:')
            if user_provided_args.strip() == 'remove':
                remove_trade()
        elif from_ == 'volume_weighted_price':
            user_provided_args = raw_input(user_prompt + '\n"vw" to calculate the volume weighted price or \'q\'to quit\n:')
            if user_provided_args.strip() == 'vw':
                calculate_volume_weighted_price()
        exit_program(user_provided_args)

        user_provided_args = [arg.strip() for arg in user_provided_args.split(',') if arg]
        if market_exchange.is_stock_registered(user_provided_args[0]):

            if len(user_provided_args) < 5:
                TradeRecord(market_exchange, user_provided_args[0], user_provided_args[1], user_provided_args[2], user_provided_args[3])
            elif len(user_provided_args) == 5:
                TradeRecord(market_exchange, user_provided_args[0], user_provided_args[1], user_provided_args[2], user_provided_args[3], user_provided_args[4])

            return add_trade(from_)
        else:
            add_stock('add_trade')
    else:
        print 'Stock Exchange Empty. Please register some stocks first.'
        # Case when add_trade is asked from the start.
        if not from_:
            from_ = 'add_trade'
        add_stock(from_)


def remove_trade():
    global market_exchange

    if not market_exchange:
        add_trade('remove_trade')
    else:
        user_provided_args = raw_input('Please provide trade for removal information in the following format:\nstock symbol,time stamp (Y-m-d H:M:S) or \'q\'to quit\n:')
        exit_program(user_provided_args)

        user_provided_args = [arg.strip() for arg in user_provided_args.split(',') if arg]
        market_exchange.remove_trade_by_symbol_date(user_provided_args[0], user_provided_args[1])

    while market_exchange.recorded_trades:
        return remove_trade()
    print 'No more trades to remove'
    sys.exit(0)


def calculate_dividend(from_='', created_stock=''):
    global market_exchange

    if not market_exchange:
        market_exchange = StockExchange('temp')
        create_stock('calculate_dividend')
    else:
        user_provided_args = raw_input('Please provide the price for stock: {}, or \'q\'to quit\n:'.format(created_stock.stock_symbol))
        exit_program(user_provided_args)
        market_exchange.add_new_stock(created_stock)
        dividend = market_exchange.dividend_yield_calculator(created_stock.stock_symbol, user_provided_args.strip())
        print 'Dividend yield for stock: {} and price: {} is: {}'.format(created_stock.stock_symbol, user_provided_args.strip(), dividend)


def calculate_p_e_ratio(created_stock=''):
    global market_exchange

    if not market_exchange:
        market_exchange = StockExchange('temp')
        create_stock('calculate_p_e_ratio')
    else:
        user_provided_args = raw_input('Please provide the price for stock: {}, or \'q\'to quit\n:'.format(created_stock.stock_symbol))
        exit_program(user_provided_args)
        market_exchange.add_new_stock(created_stock)
        p_e_ratio = market_exchange.p_e_ratio_calculator(created_stock.stock_symbol, user_provided_args.strip())
        print 'P/E ratio for stock: {} and price: {} is: {}'.format(created_stock.stock_symbol, user_provided_args.strip(), p_e_ratio)


def calculate_volume_weighted_price():
    global market_exchange

    if not market_exchange:
        add_trade('volume_weighted_price')
    else:
        user_provided_args = raw_input('Please provide the stock for which to calculate the volume weighted price in the following format:\nstock symbol, time span (optional, in minutes), or \'q\'to quit\n:')
        exit_program(user_provided_args)

        user_provided_args = [arg.strip() for arg in user_provided_args.split(',') if arg]
        if len(user_provided_args) < 2:
            market_exchange.vw_stock_price_calculator(user_provided_args[0])
        elif len(user_provided_args) == 2:
            market_exchange.vw_stock_price_calculator(user_provided_args[0], user_provided_args[1])

    # recursion to calculate again some volume weighted price
    return calculate_volume_weighted_price()


def calculate_all_share_index():
    global market_exchange

    if not market_exchange:
        add_stock('all_share_index')
    else:
        all_share_index = market_exchange.all_share_index_calculator()
        print 'All Share Index for stock exchange: {}, is: {}'.format(market_exchange.name, all_share_index)
        sys.exit(0)

# ATB, 500, sell, 555, 2017-01-05 22:14:39

# ATB, common, 8, 100, 40% preferred


# Checks if user wants to quit
def exit_program(user_input):
    if user_input in ['q', '']:
        print 'Exiting the program'
        sys.exit(0)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(
    #     description='A to sort a csv file based on a column and save the result to an output csv file')
    # parser.add_argument('-m', '--use-method',
    #                     choices=['create_exchange_market', 'create_stock', 'add_stock', 'remove_stock', 'add_trade', 'remove_trade',
    #                              'calculate_dividend', 'calculate_p_e_ratio', 'calculate_volume_weighted_price',
    #                              'calculate_all_share_index'], required=True,
    #                     help='Choose the method that you would like to run')
    # # parser.add_argument('input_file', type=argparse.FileType('r'),
    # #                     help='Input csv filename for sorting')
    # # parser.add_argument('output_file', type=argparse.FileType('w'),
    # #                     help='Sorted output csv filename')
    # args = parser.parse_args()
    #
    # main(args.use_method)
    main('calculate_all_share_index')
