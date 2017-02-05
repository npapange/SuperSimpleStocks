from distutils.core import setup

setup(
    name='simple_stock_exchange',
    version='1.5.0',
    packages=['simple_stock_exchange', 'api'],
    package_dir={'': 'SuperSimpleStocks'},
    py_modules=['console_api_runner', 'rest_api_runner', 'api.console_api', 'api.rest_api',
                'simple_stock_exchange.stock', 'simple_stock_exchange.trade_record',
                'simple_stock_exchange.stock_exchange'],
    data_files=[('', ['logging.conf']), ('', ['requirements.txt'])],
    url='https://github.com/npapange/SuperSimpleStocks',
    author='Nikitas Papangelopoulos',
    author_email='npapange@sdsc.edu',
    description='A simple stock exchange simulator.',
    requires=['enum34', 'numpy', 'flask', 'nose']
)
