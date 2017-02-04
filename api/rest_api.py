# sys.path.insert(0, os.path.abspath(".."))
from flask import Flask, request, jsonify, abort, make_response

from simple_stock_exchange import StockExchange, Stock, TradeRecord

# from simple_stock_exchange.stock_exchange import StockExchange
# from simple_stock_exchange.stock import Stock
# from simple_stock_exchange.trade_record import TradeRecord


__author__ = 'Nikitas Papangelopoulos'

# logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

app = Flask(__name__)

stock_exchange = None


@app.route('/api/create_stock_exchange', methods=['POST'])
def create_stock_exchange():
    """
    A rest wrapper for StockExchange
    """
    global stock_exchange

    json_request = request.json

    if json_request:
        # Checking if all required params were in the request
        if 'name' in json_request:
            name = json_request['name']
            # Initializing the stock exchange, only the first time. All other times the stock exchange is returned.
            if stock_exchange:
                return jsonify(stock_exchange.__dict__), 200
            else:
                # Testing if the underlying code in stock_exchange.StockExchange() executed successfully.
                try:
                    stock_exchange = StockExchange(name)
                    return jsonify({'Stock Exchange': stock_exchange.name}), 200

                except TypeError as error:
                    abort(500, error)
        else:
            abort(400, 'Parameter "name" needs to be in the request')
    else:
        abort(400)


@app.route('/api/create_stock', methods=['POST'])
def create_stock():
    """
    A rest wrapper for stock.Stock()
    """
    required_params = ['stock_symbol', 'stock_type', 'last_dividend', 'par_value']
    json_request = request.json

    if json_request:
        # Checking if all required params were in the request
        if all([True if required_param in json_request else False for required_param in required_params]):
            # Testing if the underlying code in stock.Stock() executed successfully.
            try:
                created_stock = ''
                # Stock can be created either with a fixed dividend or not.
                if len(json_request) < 5:
                    created_stock = Stock(json_request['stock_symbol'], json_request['stock_type'],
                                          json_request['last_dividend'], json_request['par_value'])
                elif len(json_request) == 5 and 'fixed_dividend' in json_request:
                    created_stock = Stock(json_request['stock_symbol'], json_request['stock_type'],
                                          json_request['last_dividend'], json_request['par_value'],
                                          json_request['fixed_dividend'])
                else:
                    abort(400, 'Fifth parameter must be "fixed_dividend".')
                return jsonify(created_stock.__dict__), 201
            except TypeError as error:
                abort(500, error)
        else:
            missing_params = set(required_params).difference(json_request)
            abort(400, 'Parameters {} needs to be in the request'.format(list(missing_params)))
    else:
        abort(400)


@app.route('/api/add_stock', methods=['POST'])
def add_stock():
    """
    A rest wrapper for StockExchange.add_new_stock()
    """
    check_stock_exchange()

    required_params = ['stock_symbol', 'stock_type', 'last_dividend', 'par_value']
    json_request = request.json

    if json_request:
        # Checking if all required params were in the request
        if all([True if required_param in json_request else False for required_param in required_params]):
            # Testing if the underlying code in StockExchange.add_new_stock() executed successfully.
            try:
                result = ''
                # Stock can be created either with a fixed dividend or not.
                if len(json_request) < 5:
                    result = stock_exchange.add_new_stock(
                        Stock(json_request['stock_symbol'], json_request['stock_type'], json_request['last_dividend'],
                              json_request['par_value']))
                elif len(json_request) == 5 and 'fixed_dividend' in json_request:
                    result = stock_exchange.add_new_stock(
                        Stock(json_request['stock_symbol'], json_request['stock_type'], json_request['last_dividend'],
                              json_request['par_value'], json_request['fixed_dividend']))
                else:
                    abort(400, 'Fifth parameter must be "fixed_dividend".')
                if result:
                    return jsonify({'Added stock': json_request['stock_symbol']}), 200
                else:
                    abort(400, 'Stock: {} is all ready in stock exchange. Please remove it first.'.format(
                        json_request['stock_symbol']))
            except TypeError as error:
                abort(500, error)
        else:
            missing_params = set(required_params).difference(json_request)
            abort(400, 'Parameters {} needs to be in the request'.format(list(missing_params)))
    else:
        abort(400)


@app.route('/api/remove_stock', methods=['POST'])
def remove_stock():
    """
    A rest wrapper for StockExchange.remove_existing_stock_by_symbol().
    """
    check_stock_exchange()

    json_request = request.json
    if json_request:
        # Checking if all required params were in the request
        if 'stock_symbol' in json_request:
            # Testing if the underlying code in StockExchange.remove_existing_stock_by_symbol() executed successfully.
            try:
                result = stock_exchange.remove_existing_stock_by_symbol(json_request['stock_symbol'])
                if result:
                    return jsonify({'Removed stock': json_request['stock_symbol']}), 200
                else:
                    abort(400, 'Please first add stock: {} in stock exchange.'.format(json_request['stock_symbol']))
            except TypeError as error:
                abort(500, error)
        else:
            abort(400, 'Parameter "stock_symbol" needs to be in the request')
    else:
        abort(400)


@app.route('/api/add_trade', methods=['POST'])
def add_trade():
    """
    A rest wrapper for StockExchange.add_new_trade()
    """
    check_stock_exchange()

    required_params = ['stock_symbol', 'quantity', 'trade_type', 'traded_price']
    json_request = request.json

    if json_request:
        # Checking if all required params were in the request
        if all([True if required_param in json_request else False for required_param in required_params]):
            # Testing if the underlying code in StockExchange.add_new_trade() executed successfully.
            try:
                result = ''
                # Stock can be created either with a fixed dividend or not.
                if len(json_request) < 5:
                    result = stock_exchange.add_new_trade(
                        TradeRecord(stock_exchange, json_request['stock_symbol'], json_request['quantity'],
                                    json_request['trade_type'], json_request['traded_price']))
                elif len(json_request) == 5 and 'time_stamp' in json_request:
                    result = stock_exchange.add_new_trade(
                        TradeRecord(stock_exchange, json_request['stock_symbol'], json_request['quantity'],
                                    json_request['trade_type'], json_request['traded_price'],
                                    json_request['time_stamp']))
                else:
                    abort(400, 'Fifth parameter must be "time_stamp".')
                if result:
                    return jsonify({'Added trade for stock': json_request['stock_symbol']}), 200
                else:
                    abort(400, 'Please first add stock: {} in stock exchange. Then add a trade for it.'.format(
                        json_request['stock_symbol']))
            except TypeError as error:
                abort(500, error)
        else:
            missing_params = set(required_params).difference(json_request)
            abort(400, 'Parameters {} needs to be in the request'.format(list(missing_params)))
    else:
        abort(400)


@app.route('/api/remove_trade', methods=['POST'])
def remove_trade():
    """
    A rest wrapper for StockExchange.remove_trade_by_symbol_date().
    """
    check_stock_exchange()

    required_params = ['stock_symbol', 'time_stamp']
    json_request = request.json

    if json_request:
        # Checking if all required params were in the request
        if all([True if required_param in json_request else False for required_param in required_params]):
            # Testing if the underlying code in StockExchange.remove_trade_by_symbol_date() executed successfully.
            try:
                result = stock_exchange.remove_trade_by_symbol_date(json_request['stock_symbol'],
                                                                    json_request['time_stamp'])
                if result:
                    return jsonify({'Removed trade for stock': json_request['stock_symbol']}), 200
                else:
                    abort(400, 'Please first add stock: {} in stock exchange. Then add a trade for it.'.format(
                        json_request['stock_symbol']))
            except TypeError as error:
                abort(500, error)
        else:
            missing_params = set(required_params).difference(json_request)
            abort(400, 'Parameters {} needs to be in the request'.format(list(missing_params)))
    else:
        abort(400)


@app.route('/api/calculate_dividend', methods=['POST'])
def calculate_dividend():
    """
    A rest wrapper for StockExchange.dividend_yield_calculator()
    """
    check_stock_exchange()

    required_params = ['stock_symbol', 'stock_price']
    json_request = request.json

    if json_request:
        # Checking if all required params were in the request
        if all([True if required_param in json_request else False for required_param in required_params]):
            # Testing if the underlying code in StockExchange.dividend_yield_calculator() executed successfully.
            try:
                dividend = stock_exchange.dividend_yield_calculator(json_request['stock_symbol'],
                                                                    json_request['stock_price'])
                if dividend:
                    return jsonify({'Dividend': dividend}), 200
                else:
                    abort(400, 'Please first add stock: {} in stock exchange.'.format(json_request['stock_symbol']))
            except TypeError as error:
                abort(500, error)
        else:
            missing_params = set(required_params).difference(json_request)
            abort(400, 'Parameters {} needs to be in the request'.format(list(missing_params)))
    else:
        abort(400)


@app.route('/api/calculate_p_e_ratio', methods=['POST'])
def calculate_p_e_ratio():
    """
    A rest wrapper for StockExchange.p_e_ratio_calculator()
    """
    check_stock_exchange()

    required_params = ['stock_symbol', 'stock_price']
    json_request = request.json

    if json_request:
        # Checking if all required params were in the request
        if all([True if required_param in json_request else False for required_param in required_params]):
            # Testing if the underlying code in StockExchange.p_e_ratio_calculator() executed successfully.
            try:
                p_e_ratio = stock_exchange.p_e_ratio_calculator(json_request['stock_symbol'],
                                                                json_request['stock_price'])
                if p_e_ratio:
                    return jsonify({'P/E ratio': p_e_ratio}), 200
                else:
                    abort(400, 'Please first add stock: {} in stock exchange.'.format(json_request['stock_symbol']))
            except TypeError as error:
                abort(500, error)
        else:
            missing_params = set(required_params).difference(json_request)
            abort(400, 'Parameters {} needs to be in the request'.format(list(missing_params)))
    else:
        abort(400)


@app.route('/api/calculate_volume_weighted_price', methods=['POST'])
def calculate_volume_weighted_price():
    """
    A rest wrapper for StockExchange.vw_stock_price_calculator()
    """
    check_stock_exchange()

    json_request = request.json

    if json_request:
        # Checking if all required params were in the request
        if 'stock_symbol' in json_request:
            stock_symbol = json_request['stock_symbol']
            # Testing if the underlying code in StockExchange.vw_stock_price_calculator() executed successfully.
            try:
                volume_weighted_price = ''
                minutes = 0
                if len(json_request) < 2:
                    minutes = 15
                    volume_weighted_price = stock_exchange.vw_stock_price_calculator(stock_symbol)
                elif len(json_request) == 2 and 'time_span' in json_request:
                    minutes = json_request['time_span']
                    volume_weighted_price = stock_exchange.vw_stock_price_calculator(json_request['stock_symbol'],
                                                                                     json_request['time_span'])
                else:
                    abort(400, 'Second parameter must be "time_span".')

                if volume_weighted_price:
                    return jsonify({'Volume Weighted Price': volume_weighted_price, 'minutes': minutes}), 200
                else:
                    abort(400, 'Please first add stock: {} and trades for it completed in the last: {} minutes.'.format(
                        json_request['stock_symbol'], minutes))

            except TypeError as error:
                abort(500, error)
        else:
            abort(400, 'Parameter "stock_symbol" needs to be in the request')
    else:
        abort(400)


@app.route('/api/calculate_all_share_index', methods=['POST'])
def calculate_all_share_index():
    """
    A rest wrapper for StockExchange.all_share_index_calculator()
    """
    check_stock_exchange()
    # Testing if the underlying code in StockExchange.all_share_index_calculator() executed successfully.
    try:
        all_share_index = stock_exchange.all_share_index_calculator()
        if all_share_index:
            return jsonify({'All share index': all_share_index}), 200
        else:
            abort(400, 'Please first add some stocks and trades in stock exchange.')
    except TypeError as error:
        abort(500, error)


def check_stock_exchange():
    """
    Small convenience method that checks if a stock exchange object exits
    and if not, throws a custom 400 error.
    """
    if not stock_exchange:
        abort(400, 'Please create a stock exchange first.')


@app.errorhandler(400)
def not_found(error):
    """
    A method to return a json formatted custom error 400
    :param error: A custom error message
    :type error: BadRequest
    """
    print type(error)
    return make_response(jsonify({'error': error.description}), 400)


@app.errorhandler(404)
def not_found():
    """
    A method to return a json formatted custom error 404
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def not_found(error):
    """
    A method to return a json formatted custom error 500
    :param error: The error message from executing code in teh simple_stock_exchange package.
    :type error: BadRequest
    """
    return make_response(jsonify({'error': error.description}), 404)

#
# if __name__ == '__main__':
#     app.run()
