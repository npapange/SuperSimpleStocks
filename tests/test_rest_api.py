#!/usr/bin/python

import unittest
import logging.config
import json
from api import rest_api

__author__ = 'Nikitas Papangelopoulos'

logging.config.fileConfig('/SuperSimpleStocks/logging.conf', disable_existing_loggers=False)


class TestRestApi(unittest.TestCase):

    def setUp(self):
        self.app = rest_api.app.test_client()
        self.app.testing = True

    def test_create_stock_exchange(self):
        response = self.app.post('http://localhost:5000/api/create_stock_exchange',
                                 data=json.dumps({'name': 'test_stock_exchange'}),
                                 content_type='application/json')
        self.assertEqual(json.loads(response.get_data()), {'Stock Exchange': 'test_stock_exchange'})
        self.assertEqual(response.status_code, 200)

        response0 = self.app.post('http://localhost:5000/api/create_stock_exchange',
                                  data=json.dumps({'name': 'test_stock_exchange'}),
                                  content_type='application/json')
        self.assertEqual(json.loads(response0.get_data()), {
            "all_share_index": "",
            "name": "test_stock_exchange",
            "recorded_trades": {},
            "registered_stocks": {}
        })
        self.assertEqual(response0.status_code, 200)

        response1 = self.app.post('http://localhost:5000/api/create_stock_exchange',
                                  data=json.dumps({'type': 'test_stock_exchange'}),
                                  content_type='application/json')
        self.assertEqual(json.loads(response1.get_data()), {"error": "Parameter \"name\" needs to be in the request"})
        self.assertEqual(response1.status_code, 400)

        response2 = self.app.post('http://localhost:5000/api/create_stock_exchange')
        self.assertEqual(response2.status_code, 400)

    def test_create_stock(self):
        response = self.app.post('http://localhost:5000/api/create_stock',
                                 data=json.dumps({
                                     "stock_symbol": "POP",
                                     "stock_type": "common",
                                     "last_dividend": "8",
                                     "par_value": "100"
                                 }),
                                 content_type='application/json')
        self.assertEqual(json.loads(response.get_data()), {
            "created_successfully": True,
            "current_price": "",
            "current_price_timestamp": "",
            "dividend_yield": "",
            "fixed_dividend": None,
            "last_dividend": 8,
            "p_e_ratio": "",
            "par_value": 100,
            "stock_symbol": "POP",
            "stock_type": "common"
        })
        self.assertEqual(response.status_code, 201)

        response0 = self.app.post('http://localhost:5000/api/create_stock',
                                  data=json.dumps({
                                      "stock_symbol": "GIN",
                                      "stock_type": "preferred",
                                      "last_dividend": "8",
                                      "par_value": "100",
                                      "fixed_dividend": "0.02"
                                  }),
                                  content_type='application/json')
        self.assertEqual(json.loads(response0.get_data()), {
            "created_successfully": True,
            "current_price": "",
            "current_price_timestamp": "",
            "dividend_yield": "",
            "fixed_dividend": 0.02,
            "last_dividend": 8,
            "p_e_ratio": "",
            "par_value": 100,
            "stock_symbol": "GIN",
            "stock_type": "preferred"
        })
        self.assertEqual(response0.status_code, 201)

        response1 = self.app.post('http://localhost:5000/api/create_stock',
                                  data=json.dumps({
                                      "stock_type": "common",
                                      "last_dividend": "8",
                                      "par_value": "100"
                                  }),
                                  content_type='application/json')
        self.assertEqual(json.loads(response1.get_data()),
                         {"error": "Parameters ['stock_symbol'] needs to be in the request"})
        self.assertEqual(response1.status_code, 400)

        response2 = self.app.post('http://localhost:5000/api/create_stock')
        self.assertEqual(response2.status_code, 400)

        response3 = self.app.post('http://localhost:5000/api/create_stock',
                                  data=json.dumps({
                                      "stock_symbol": "GIN",
                                      "stock_type": "preferred",
                                      "last_dividend": "8",
                                      "par_value": "100",
                                      "test": "0.02"
                                  }),
                                  content_type='application/json')
        self.assertEqual(json.loads(response3.get_data()), {"error": "Fifth parameter must be \"fixed_dividend\"."})
        self.assertEqual(response3.status_code, 400)

    def test_add_stock(self):
        self.app.post('http://localhost:5000/api/create_stock_exchange',
                      data=json.dumps({'name': 'test_stock_exchange'}),
                      content_type='application/json')

        response = self.app.post('http://localhost:5000/api/add_stock',
                                 data=json.dumps({
                                     "stock_symbol": "POP",
                                     "stock_type": "common",
                                     "last_dividend": "8",
                                     "par_value": "100"
                                 }),
                                 content_type='application/json')
        self.assertEqual(json.loads(response.get_data()), {"Added stock": "POP"})
        self.assertEqual(response.status_code, 200)

        response0 = self.app.post('http://localhost:5000/api/add_stock',
                                  data=json.dumps({
                                      "stock_symbol": "GIN",
                                      "stock_type": "preferred",
                                      "last_dividend": "8",
                                      "par_value": "100",
                                      "fixed_dividend": "0.02"
                                  }),
                                  content_type='application/json')
        self.assertEqual(json.loads(response0.get_data()), {"Added stock": "GIN"})
        self.assertEqual(response0.status_code, 200)

        response1 = self.app.post('http://localhost:5000/api/add_stock',
                                  data=json.dumps({
                                      "stock_type": "common",
                                      "last_dividend": "8",
                                      "par_value": "100"
                                  }),
                                  content_type='application/json')
        self.assertEqual(json.loads(response1.get_data()),
                         {"error": "Parameters ['stock_symbol'] needs to be in the request"})
        self.assertEqual(response1.status_code, 400)

        response2 = self.app.post('http://localhost:5000/api/add_stock')
        self.assertEqual(response2.status_code, 400)

        response3 = self.app.post('http://localhost:5000/api/add_stock',
                                  data=json.dumps({
                                      "stock_symbol": "GIN",
                                      "stock_type": "preferred",
                                      "last_dividend": "8",
                                      "par_value": "100",
                                      "test": "0.02"
                                  }),
                                  content_type='application/json')
        self.assertEqual(json.loads(response3.get_data()), {"error": "Fifth parameter must be \"fixed_dividend\"."})
        self.assertEqual(response3.status_code, 400)

    def test_remove_stock(self):
        self.app.post('http://localhost:5000/api/create_stock_exchange',
                      data=json.dumps({'name': 'test_stock_exchange'}),
                      content_type='application/json')

        response = self.app.post('http://localhost:5000/api/remove_stock',
                                 data=json.dumps({'stock_symbol': 'POP'}),
                                 content_type='application/json')
        self.assertEqual(json.loads(response.get_data()), {'error': 'Please first add stock: POP in stock exchange.'})
        self.assertEqual(response.status_code, 400)

        self.app.post('http://localhost:5000/api/add_stock',
                      data=json.dumps({
                          "stock_symbol": "POP",
                          "stock_type": "common",
                          "last_dividend": "8",
                          "par_value": "100"
                      }),
                      content_type='application/json')

        response0 = self.app.post('http://localhost:5000/api/remove_stock',
                                  data=json.dumps({'stock_symbol': 'POP'}),
                                  content_type='application/json')
        self.assertEqual(json.loads(response0.get_data()), {"Removed stock": "POP"})
        self.assertEqual(response0.status_code, 200)

        response1 = self.app.post('http://localhost:5000/api/remove_stock',
                                  data=json.dumps({'type': 'POP'}),
                                  content_type='application/json')
        self.assertEqual(json.loads(response1.get_data()),
                         {"error": "Parameter \"stock_symbol\" needs to be in the request"})
        self.assertEqual(response1.status_code, 400)

        response2 = self.app.post('http://localhost:5000/api/remove_stock')
        self.assertEqual(response2.status_code, 400)

    def test_add_trade(self):
        self.app.post('http://localhost:5000/api/create_stock_exchange',
                      data=json.dumps({'name': 'test_stock_exchange'}),
                      content_type='application/json')

        response = self.app.post('http://localhost:5000/api/add_trade',
                                 data=json.dumps({
                                     "quantity": "300",
                                     "trade_type": "buy",
                                     "stock_symbol": "POP",
                                     "traded_price": "150",
                                 }),
                                 content_type='application/json')
        self.assertEqual(json.loads(response.get_data()),
                         {"error": "Please first add stock: POP in stock exchange. Then add a trade for it."})
        self.assertEqual(response.status_code, 400)

        self.app.post('http://localhost:5000/api/add_stock',
                      data=json.dumps({
                          "stock_symbol": "POP",
                          "stock_type": "common",
                          "last_dividend": "8",
                          "par_value": "100"
                      }),
                      content_type='application/json')

        response0 = self.app.post('http://localhost:5000/api/add_trade',
                                  data=json.dumps({
                                      "quantity": "300",
                                      "trade_type": "buy",
                                      "stock_symbol": "POP",
                                      "traded_price": "150",
                                  }),
                                  content_type='application/json')
        self.assertEqual(json.loads(response0.get_data()), {"Added trade for stock": "POP"})
        self.assertEqual(response0.status_code, 200)

        response1 = self.app.post('http://localhost:5000/api/add_trade',
                                  data=json.dumps({
                                      "quantity": "300",
                                      "trade_type": "buy",
                                      "stock_symbol": "POP",
                                      "traded_price": "150",
                                      "time_stamp": "2017-02-04 23:30:39"
                                  }),
                                  content_type='application/json')
        self.assertEqual(json.loads(response1.get_data()), {"Added trade for stock": "POP"})
        self.assertEqual(response1.status_code, 200)

        response2 = self.app.post('http://localhost:5000/api/add_trade',
                                  data=json.dumps({
                                      "quantity": "300",
                                      "trade_type": "buy",
                                      "stock_symbol": "POP",
                                  }),
                                  content_type='application/json')
        self.assertEqual(json.loads(response2.get_data()),
                         {"error": "Parameters ['traded_price'] needs to be in the request"})
        self.assertEqual(response2.status_code, 400)

        response2 = self.app.post('http://localhost:5000/api/add_trade')
        self.assertEqual(response2.status_code, 400)

        response3 = self.app.post('http://localhost:5000/api/add_trade',
                                  data=json.dumps({
                                      "quantity": "300",
                                      "trade_type": "buy",
                                      "stock_symbol": "POP",
                                      "traded_price": "150",
                                      "test": "2017-02-04 23:30:39"
                                  }),
                                  content_type='application/json')
        self.assertEqual(json.loads(response3.get_data()), {"error": "Fifth parameter must be \"time_stamp\"."})
        self.assertEqual(response3.status_code, 400)

    def test_remove_trade(self):
        self.app.post('http://localhost:5000/api/create_stock_exchange',
                      data=json.dumps({'name': 'test_stock_exchange'}),
                      content_type='application/json')

        response = self.app.post('http://localhost:5000/api/remove_trade',
                                 data=json.dumps({'stock_symbol': 'POP', 'time_stamp': '2017-02-04 23:30:39'}),
                                 content_type='application/json')
        self.assertEqual(json.loads(response.get_data()),
                         {'error': 'Please first add stock: POP in stock exchange. Then add a trade for it.'})
        self.assertEqual(response.status_code, 400)

        self.app.post('http://localhost:5000/api/add_stock',
                      data=json.dumps({
                          "stock_symbol": "POP",
                          "stock_type": "common",
                          "last_dividend": "8",
                          "par_value": "100"
                      }),
                      content_type='application/json')

        self.app.post('http://localhost:5000/api/add_trade',
                      data=json.dumps({
                          "quantity": "300",
                          "trade_type": "buy",
                          "stock_symbol": "POP",
                          "traded_price": "150",
                          "time_stamp": "2017-02-04 23:30:39"
                      }),
                      content_type='application/json')

        response0 = self.app.post('http://localhost:5000/api/remove_trade',
                                  data=json.dumps({'stock_symbol': 'POP', 'time_stamp': '2017-02-04 23:30:39'}),
                                  content_type='application/json')
        self.assertEqual(json.loads(response0.get_data()), {"Removed trade for stock": "POP"})
        self.assertEqual(response0.status_code, 200)

        response1 = self.app.post('http://localhost:5000/api/remove_trade',
                                  data=json.dumps({'stock_symbol': 'POP', 'test': '2017-02-04 23:30:39'}),
                                  content_type='application/json')
        self.assertEqual(json.loads(response1.get_data()),
                         {"error": "Parameters ['time_stamp'] needs to be in the request"})
        self.assertEqual(response1.status_code, 400)

        response2 = self.app.post('http://localhost:5000/api/remove_trade')
        self.assertEqual(response2.status_code, 400)

    def test_calculate_dividend(self):
        self.app.post('http://localhost:5000/api/create_stock_exchange',
                      data=json.dumps({'name': 'test_stock_exchange'}),
                      content_type='application/json')

        response = self.app.post('http://localhost:5000/api/calculate_dividend',
                                 data=json.dumps({"stock_symbol": "POP", "stock_price": "130"}),
                                 content_type='application/json')
        self.assertEqual(json.loads(response.get_data()), {'error': 'Please first add stock: POP in stock exchange.'})
        self.assertEqual(response.status_code, 400)

        self.app.post('http://localhost:5000/api/add_stock',
                      data=json.dumps({
                          "stock_symbol": "POP",
                          "stock_type": "common",
                          "last_dividend": "8",
                          "par_value": "100"
                      }),
                      content_type='application/json')

        response0 = self.app.post('http://localhost:5000/api/calculate_dividend',
                                  data=json.dumps({"stock_symbol": "POP", "stock_price": "130"}),
                                  content_type='application/json')
        self.assertEqual(json.loads(response0.get_data()), {"Dividend": 0.062})
        self.assertEqual(response0.status_code, 200)

        response1 = self.app.post('http://localhost:5000/api/calculate_dividend',
                                  data=json.dumps({"stock_symbol": "POP"}),
                                  content_type='application/json')
        self.assertEqual(json.loads(response1.get_data()),
                         {"error": "Parameters ['stock_price'] needs to be in the request"})
        self.assertEqual(response1.status_code, 400)

        response2 = self.app.post('http://localhost:5000/api/calculate_dividend')
        self.assertEqual(response2.status_code, 400)

    def test_calculate_p_e_ratio(self):
        self.app.post('http://localhost:5000/api/create_stock_exchange',
                      data=json.dumps({'name': 'test_stock_exchange'}),
                      content_type='application/json')

        response = self.app.post('http://localhost:5000/api/calculate_p_e_ratio',
                                 data=json.dumps({"stock_symbol": "POP", "stock_price": "130"}),
                                 content_type='application/json')
        self.assertEqual(json.loads(response.get_data()), {'error': 'Please first add stock: POP in stock exchange.'})
        self.assertEqual(response.status_code, 400)

        self.app.post('http://localhost:5000/api/add_stock',
                      data=json.dumps({
                          "stock_symbol": "POP",
                          "stock_type": "common",
                          "last_dividend": "8",
                          "par_value": "100"
                      }),
                      content_type='application/json')

        response0 = self.app.post('http://localhost:5000/api/calculate_p_e_ratio',
                                  data=json.dumps({"stock_symbol": "POP", "stock_price": "130"}),
                                  content_type='application/json')
        self.assertEqual(json.loads(response0.get_data()), {"P/E ratio": 16.25})
        self.assertEqual(response0.status_code, 200)

        response1 = self.app.post('http://localhost:5000/api/calculate_p_e_ratio',
                                  data=json.dumps({"stock_symbol": "POP"}),
                                  content_type='application/json')
        self.assertEqual(json.loads(response1.get_data()),
                         {"error": "Parameters ['stock_price'] needs to be in the request"})
        self.assertEqual(response1.status_code, 400)

        response2 = self.app.post('http://localhost:5000/api/calculate_p_e_ratio')
        self.assertEqual(response2.status_code, 400)

    def test_calculate_all_share_index(self):
        self.app.post('http://localhost:5000/api/create_stock_exchange',
                      data=json.dumps({'name': 'test_stock_exchange'}),
                      content_type='application/json')

        response = self.app.post('http://localhost:5000/api/calculate_all_share_index')
        self.assertEqual(json.loads(response.get_data()),
                         {'error': 'Please first add some stocks and trades in stock exchange.'})
        self.assertEqual(response.status_code, 400)

        self.app.post('http://localhost:5000/api/add_stock',
                      data=json.dumps({
                          "stock_symbol": "POP",
                          "stock_type": "common",
                          "last_dividend": "8",
                          "par_value": "100"
                      }),
                      content_type='application/json')

        self.app.post('http://localhost:5000/api/add_stock',
                      data=json.dumps({
                          "stock_symbol": "TEA",
                          "stock_type": "common",
                          "last_dividend": "0",
                          "par_value": "100"
                      }),
                      content_type='application/json')

        self.app.post('http://localhost:5000/api/add_trade',
                      data=json.dumps({
                          "quantity": "300",
                          "trade_type": "buy",
                          "stock_symbol": "POP",
                          "traded_price": "150",
                      }),
                      content_type='application/json')

        self.app.post('http://localhost:5000/api/add_trade',
                      data=json.dumps({
                          "quantity": "300",
                          "trade_type": "sell",
                          "stock_symbol": "TEA",
                          "traded_price": "180",
                      }),
                      content_type='application/json')

        response0 = self.app.post('http://localhost:5000/api/calculate_all_share_index')
        self.assertEqual(json.loads(response0.get_data()), {'All share index': 164.317})
        self.assertEqual(response0.status_code, 200)

    def test_calculate_volume_weighted_price(self):
        self.app.post('http://localhost:5000/api/create_stock_exchange',
                      data=json.dumps({'name': 'test_stock_exchange'}),
                      content_type='application/json')

        response = self.app.post('http://localhost:5000/api/calculate_volume_weighted_price',
                                 data=json.dumps({"stock_symbol": "POP", "time_span": "5"}),
                                 content_type='application/json')
        self.assertEqual(json.loads(response.get_data()),
                         {'error': 'Please first add stock: POP and trades for it completed in the last: 5 minutes.'})
        self.assertEqual(response.status_code, 400)

        self.app.post('http://localhost:5000/api/add_stock',
                      data=json.dumps({
                          "stock_symbol": "POP",
                          "stock_type": "common",
                          "last_dividend": "8",
                          "par_value": "100"
                      }),
                      content_type='application/json')

        self.app.post('http://localhost:5000/api/add_trade',
                      data=json.dumps({
                          "quantity": "300",
                          "trade_type": "buy",
                          "stock_symbol": "POP",
                          "traded_price": "150",
                      }),
                      content_type='application/json')

        self.app.post('http://localhost:5000/api/add_trade',
                      data=json.dumps({
                          "quantity": "200",
                          "trade_type": "sell",
                          "stock_symbol": "POP",
                          "traded_price": "180",
                      }),
                      content_type='application/json')

        response0 = self.app.post('http://localhost:5000/api/calculate_volume_weighted_price',
                                  data=json.dumps({"stock_symbol": "POP"}),
                                  content_type='application/json')
        self.assertEqual(json.loads(response0.get_data()), {'Volume Weighted Price': 162.0, 'minutes': 15})
        self.assertEqual(response0.status_code, 200)

        response1 = self.app.post('http://localhost:5000/api/calculate_volume_weighted_price',
                                  data=json.dumps({"stock_symbol": "POP", "test": "2"}),
                                  content_type='application/json')
        self.assertEqual(json.loads(response1.get_data()), {"error": 'Second parameter must be "time_span".'})
        self.assertEqual(response1.status_code, 400)

        response2 = self.app.post('http://localhost:5000/api/calculate_volume_weighted_price')
        self.assertEqual(response2.status_code, 400)
