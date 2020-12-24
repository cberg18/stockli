#! /usr/bin/env python3
import sys
import os
import alpaca_trade_api as tradeapi

try:
    import config
except ModuleNotFoundError:
    print('The config file seems to be missing.')
    print('Use ./stockli.py --config for help setting up the config file.')
    quit()

API_KEY = config.API_KEY
API_SECRET = config.API_SECRET
BASE_URL = config.BASE_URL

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL)
account = api.get_account()

logFile = '/stockli.log'
oldLogFile = '/var/log/stockli.log.old'
LOGSIZE = 10000000

# check if log file needs to be rotated
if os.path.exists(logFile) and os.path.getsize(logFile) > LOGSIZE:
    if os.path.exists(oldLogFile):
        os.remove(oldLogFile)
    print("Rotating Log File")
    os.rename(logFile, oldLogFile)
    os.remove(logFile)


def helpString():
    help_string = '''
    Stockli is a command line wrapper for trading stocks with Alpaca.
    This tool requires an active account with Alpaca.

    Usage: ./stockli.py [OPTION]...

    Options:
     -h, --help                     prints this page and exits.
     -u, --update                   checks for updates.
     -s [SYMBOL]                    grabs relevant information for [SYMBOL]
     --market-status                returns if market is open or closed
     --list-current-positions       list all open positions
     --buy [SYMBOL] [QUANTITY]      buy specified quantitiy of a stock

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


if __name__ == '__main__':
    if (sys.argv[1] == '-h') or (sys.argv[1] == '--help'):
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
        clock = api.get_clock()
        if clock == True:
            print('The market is currently open.')
        else:
            print('The market is currently closed.')

    elif (sys.argv[1] == '--list-current-positions'):
        positions = api.list_positions()

        if len(positions) == 0:
            print('You have no active positions.')
        else:
            for position in positions:
                print(position.symbol + ': ' + position.qty + ' @ $' + str(round(float(position.avg_entry_price ))))

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

    else:
        print('Specified option not recognized. Do main.py -h or --help for help.')
