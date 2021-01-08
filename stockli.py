#! /usr/bin/env python3
# TODO: trend detector
# TODO: calc current rating
# TODO: check if you have sufficient funds to process a buy order

import sys
import os
import time
import alpaca_trade_api as tradeapi

try:
    import config
except ModuleNotFoundError:
    print('The config file seems to be missing.')
    print('Use ./stockli.py --config for help setting up the config file.')
    quit()

trading_type = 'paper'

API_KEY = config.API_KEY
API_SECRET = config.API_SECRET
BASE_URL = config.BASE_URL

# initialize connection to api and get market status
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL)
account = api.get_account()
market_status = api.get_clock().is_open

intervals = ['1m', '2m', '5m', '15m', '30m', '60m']


def helpString():
    help_string = '''
    Stockli is a command line wrapper for trading stocks with Alpaca.
    This tool requires an active account with Alpaca.

    Usage: ./stockli.py [OPTION]...

    Options:
    -h, --help                                      prints this page and exits.
    -u, --update                                    checks for updates.
    -s [SYMBOL]                                     grabs relevant information for [SYMBOL]
    --market-status                                 returns if market is open or closed
    --list-current-positions                        list all open positions
    --buy [SYMBOL] [QUANTITY]                       buy specified quantitiy of a stock
    --sell [SYMBOL] [QUANTITY]                      sell specified quantity of a stock
    --track [SYMBOL] [PERIOD]                       track a symbol at sepcified interval until interupted, default 2m (valid periods: 1m,2m,5m,15m,30m,60m)
    --trade-type                                    gets currently used trading api, paper or live. CAUTION: AT THIS TIME, STOCKLI HAS NOT BEEN TESTED IN A LIVE ENVIRONMENT. USE AT YOUR OWN RISK.

    stockli is pre-pre-pre-pre-pre alpha and comes with NO WARRANTY.
    If you're seeing this, you probably shouldn't be. Shame on you.
    At this time functionality is incomplete and in development.

    See https://alpaca.markets/docs/api-documentation/api-v2/ for more information.
    '''
    print(help_string)
    return


def configHelpString():
    config = '''
    Stockli expects a config file in its root directory (i.e. ./stockli/config.py)
    with the following information:

    BASE_URL = 'https://paper-api.alpaca.markets' OR 'https://api.alpaca.markets'
    API_KEY = 'YOUR-API-KEY-HERE'
    API_SECRET = 'YOUR-API-SECRET-HERE'

    If you are using the paper endpoint, the api key and secret must match that endpoint.
    See the web console for api key and secret.
    '''
    print(config)
    return


def tracker(symbol, interval='2m'):
    import yfinance as yf
    # this function is for tracking stock price at specified interval
    # throughout the day.
    print('Starting tracking for ' + symbol +
          ' at ' + interval + ' intervals.')
    ticker_last = 0
    ticker_current = 0
    ticker_change = 0
    if interval not in intervals:
        print('Specified interval, ' + interval +
              ', is not a valid interval. Valid intervals are: ')
        print(intervals)
        return

    while market_status == True:

        ticker_current = yf.Ticker(symbol).history(
            period='1d', interval='2m').iloc[-1]['Close']
        print(symbol + ': $' + str(ticker_current) +
              ' Change: ' + str(ticker_change) + '%')
        ticker_last = ticker_current
        if not ticker_change == 0:
            ticker_change = (
                (ticker_last - ticker_current) / ticker_last) * 100
        time.sleep(int(interval[:-1]) * 60)

    else:
        print('The market has closed. ')
        return


if __name__ == '__main__':
    if (len(sys.argv) == 1) or (sys.argv[1] == '-h') or (sys.argv[1] == '--help'):
        helpString()

    elif (sys.argv[1] == '-u') or (sys.argv[1] == '--update'):
        o = os.system('./update.sh')

    elif (sys.argv[1] == '--config'):
        configHelpString()

    elif (sys.argv[1] == '-s'):
        import utils.class_gen
        print(sys.argv[2].upper() + ' closed at $' +
              str(round(utils.class_gen.Symbol(sys.argv[2]).lastClose, 2)))

    elif (sys.argv[1] == '--market-status'):
        if market_status == True:
            print('The market is currently open.')
        else:
            print('The market is currently closed.')

    elif (sys.argv[1] == '--list-current-positions'):
        positions = api.list_positions()

        if len(positions) == 0:
            print('You have no active positions.')
        else:
            for position in positions:
                print(position.symbol + ': ' + position.qty + ' @ $' +
                      str(round(float(position.avg_entry_price))))

    elif (sys.argv[1] == '--buy'):
        print('Attempting to buy ' +
              sys.argv[3] + ' shares of ' + sys.argv[2].upper())
        order = api.submit_order(
            symbol=sys.argv[2].upper(),
            side='buy',
            type='market',
            qty=sys.argv[3],
            time_in_force='day'
        )
        if order.status == 'filled':
            print('Your order was filled successfully')

        elif order.status == 'partially_filled':
            print('Your order has been partially filled.')

        elif order.status == 'accepted':
            print(
                'Your order was accepted by Alpaca, but has not ben routed to be executed.')

    elif (sys.argv[1] == '--sell'):
        try:
            positions = api.get_position(sys.argv[2].upper())
        except BaseException:
            print('You don\'t have any positions of ' + sys.argv[2])

        if int(sys.argv[3]) > int(positions.qty):
            print('You have requested to sell more positions than you own. Use --list-current-positions to find your currently held positions.')
        else:
            order = api.submit_order(
                symbol=sys.argv[2].upper(),
                side='sell',
                type='market',
                qty=sys.argv[3],
                time_in_force='day'
            )
            if order.status == 'filled':
                print('Your order was filled successfully')

            elif order.status == 'partially_filled':
                print('Your order has been partially filled.')

            elif order.status == 'accepted':
                print(
                    'Your order was accepted by Alpaca, but has not ben routed to be executed.')

    elif (sys.argv[1] == '--track'):
        if market_status == False:
            print('The market is currently closed. ')
            quit()

        if len(sys.argv) < 3:
            print(
                'Not enough arguments. Please specify a symbol to track or use --help for more info.')
            quit()

        if len(sys.argv) == 4:
            period = str(sys.argv[3])
            tracker(sys.argv[2].upper(), period)

        else:
            print('No period specified, using default at 2m.')
            period = '2m'
            tracker(sys.argv[2].upper(), period)

    elif (sys.argv[1] == '--trade-type'):
        if len(sys.argv) < 3:
            print('Not enough arguments, use -h or --help for more information. ')
            quit()
        if sys.argv[2].lower() == 'current':
            print('Stockli is set to use the ' + trading_type + ' endpoint.')
#        if sys.argv[2].lower() == 'set' and len(sys.argv) < 4 : print('Please specify either live or paper api. ')
#        if sys.argv[2].lower() == 'set' and ((sys.argv[3].lower() == 'live') or (sys.argv[3].lower() == 'paper')) : config.trading_type = trading_type = sys.argv[3].lower()

    else:
        print('Specified option not recognized. Do main.py -h or --help for help.')
