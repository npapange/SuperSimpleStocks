<b>SuperSimpleStocks</b><br />
<br />
<br />
<b>Description:</b><br />
    A simple application that simulates a stock exchange. It has the ability to create and register stocks (Stock class)<br />
and trades (TradeRecord class) for these stocks in a stock exchange object. The class 'stock_exchange' contains<br />
methods to add and remove stocks and trades, as well as some helper methods that execute some common tasks and checks.<br />
Also, methods are provided to calculate the following:<br />
- For a given stock:<br />
    -calculate the dividend yield.<br />
    -calculate the P/E Ratio.<br />
    -record a trade, with timestamp, quantity of shares, buy or sell indicator and price.<br />
    -Calculate Stock Price based on trades recorded in past 15 minutes.<br />
- Calculate the stock exchange's All Share Index of prices for all stocks.<br />
<br />
Lastly, the project also contains an 'api' with two APIs to easily access and use the modules of the main package<br />
'simple_stock_exchange'. One console api, that a user can run and perform all the available functions of stock_exchange<br />
and a module that exposes a RESTful API server that also gives access to the stock_exchange functionality.<br />
<br />
<br />
<b>Notes on Implementation:</b><br />
    The Stock class has an optional stock_exchange object parameter. This is offered so that if the user creates a stock<br />
because he wishes to add it to stock_exchange, this can be done in one step, if he also provides said stock_exchange<br />
object. In the case he or she just wants to create a stock, independently of a stock exchange, he can also do that by<br />
not providing this particular parameter. This can be useful if for example he just wants to calculate the dividend yield<br />
of that stock. The stock_type is implemented as an enum, since there are only two standard available "common or preferred".<br />

For the Trade class the stock_exchange object parameter is required since a trade can only happen inside a stock <br />
exchange. So, during object creation, it is also automatically registered to the provided stock exchange. Also, there<br />
is also a check implemented that will not allow a trade for a non existing stock to be registered in the stock exchange,<br />
since this would not make any sense. Lastly, there is an optional time_stamp parameter that corresponds to the time the<br />
trade occurred. If the user doesn't provide one, then the current time stamp will be automatically provided. The trade_type<br />is implemented as an enum, since there are only two standard available "buy or sell".<br />

If the user asks for a function that has prerequisites, the console API will automatically guide him with <br />
informative prompts to first provide the required data in a specific format and then execute the function he requested.<br />
In a similar case the REST API will return an error message, detailing the missing data.<br />

All time stamps where ever they are used, need to be in teh following format: 2017-02-05 22:14:39.<br />
    
Numpy is used for most calculations because it is faster than Python and has many convenience methods that<br />
simplify tasks.<br />

The logging configuration is located in the "logging.conf" file. It prints messages in the console as well as saves<br />
the log messages in a file called Stocks.log. So as to not "bombard" the user with two many logging information, the log<br />
level for the console output is set to "INFO", whereas for the log file it is set to "DEBUG", so that all statements are<br />
saved in a file.<br />
<br />
<br />
<b>Requirements:</b><br />
    Python 2.7 + (tested on 2.7.12)<br />
<br />
<br />
<b>Installation:</b><br />
    To install the application just check out the code and run "setup.py install". Also a requirements.txt file is provided<br />
that can be used to independently install all required packages by running the command "pip install -r requirements.txt".<br />
<br />
<br />
<b>Usage:</b><br />
    There are two runner scripts provided for each of the APIs:<br />
        - For the console API the script "console_api_runner.py" is provided. The user needs to run it with a single<br />
          specific parameter denoting the function she wants to use. e.g. "console_api_runner.py -m calculate_dividend".<br />
          A list of all implemented methods and a short description can be obtained by typing "console_api_runner.py -h".<br />
        - For the REST API the script "rest_api_runner.py" is provided. When this is run, it will start a flask server<br />
          (at the default base URL http://127.0.0.1:5000/) that can accept POST json requests to URLs that correspond to<br />
          the stock_exchange module's methods.<br />
          
    More information and additional details on usage can be found in the doc strings.<br />
<br />
<br />
<b>Tests:</b><br /><br />
    For testing the application there are unit tests provided in the tests folder. To run all tests, a convenience method<br />
is provided in the root directory: "test_runner.py". This will run all tests for the main "simple_stock_module".<br />
Coverage is 100%. Also tests can be run using "nose" as following: "cd path/to/project" and "nosetests".<br />

   There are also unit tests provided for the REST API. These are run with the "test_rest_api.py" script. Because the<br />
flask test server cannot accept many concurrent requests, please run the tests individually through an IDE.<br />
