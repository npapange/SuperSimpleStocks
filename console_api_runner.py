#!/usr/bin/python

import argparse
import logging.config

from api import console_api

__author__ = 'Nikitas Papangelopoulos'

logging.config.fileConfig('/SuperSimpleStocks/logging.conf', disable_existing_loggers=False)

# Getting the user's input.
parser = argparse.ArgumentParser(
    description='A to sort a csv file based on a column and save the result to an output csv file')
parser.add_argument('-m', '--use-method',
                    choices=['create_exchange_market', 'create_stock', 'add_stock', 'remove_stock', 'add_trade',
                             'remove_trade', 'calculate_dividend', 'calculate_p_e_ratio',
                             'calculate_volume_weighted_price', 'calculate_all_share_index'], required=True,
                    help='Choose the method that you would like to run')
args = parser.parse_args()

console_api.main(args.use_method)
console_api.main('calculate_all_share_index')
