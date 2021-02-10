#! /usr/bin/env python3
# TODO: trend detector
# TODO: calc current rating
# TODO: check if you have sufficient funds to process a buy order


import os
import sys
import time

import utils.api_connect


try:
    import config
except ModuleNotFoundError:
    print('The config file seems to be missing.')
    print('Use ./stockli.py --config help for help setting up the config file.')
    quit()


# valid intervals for --track
intervals = ['1m', '2m', '5m', '15m', '30m', '60m']


def helpString():
    help_string = '''
    Stockli is a command line wrapper for trading stocks with Alpaca.
    This tool requires an active account with Alpaca.

    Usage: ./stockli.py [OPTION]...

    Options:
    -h, --help                                      prints this page and exits.
    -s [SYMBOL]                                     grabs relevant information for [SYMBOL]
    -u, --update                                    checks for updates.
    --buy [SYMBOL] [QUANTITY]                       buy specified quantitiy of a stock
    --config                                        modify config, --config help for more information
    --list-current-positions                        list all open positions
    --market-status                                 returns if market is open or closed
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
    Stockli expects a config file in its root directory (i.e. ./stockli/config.ini)
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
    '''
    This function is for tracking stock price at specified interval
    throughout the day.
    '''

    import yfinance as yf

    # initialize api connection
    api = utils.api_connect.alpaca_connection()
    market_status = api.get_clock().is_open

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
        print(symbol + ': $%.2f' % (ticker_current))
        ticker_last = ticker_current
        if not ticker_change == 0:
            ticker_change = (
                (ticker_last - ticker_current) / ticker_last) * 100

        if market_status == False:
            market_status = False

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
        # TODO: Interactive config
        if len(sys.argv) < 3:
            configHelpString()

        elif sys.argv[2] == 'help':
            configHelpString()

        elif sys.argv[2] == 'configured-accounts':
            accounts = config.list_configured_accounts()
            print('Currently configured accounts: ')
            for i in accounts:
                print(i)

        elif sys.argv[2] == 'add-account':
            account_name = input('Enter account name: ')
            api_key = input('Enter API Key: ')
            api_secret = input('Enter API Secret: ')
            base_url = input('Enter Base URL: ')
            config.add_account_details(
                account_name.upper(), api_key, api_secret, base_url)

        elif sys.argv[2] == 'remove-account':
            account_name = input('Enter name of account to remove: ')
            config.remove_account_details(account_name.upper())

    elif (sys.argv[1] == '-s'):
        import utils.class_gen
        print(sys.argv[2].upper() + ' closed at $%.2f' %
              (utils.class_gen.Symbol(sys.argv[2]).lastClose))

    elif (sys.argv[1] == '-a'):
        import utils.analytics
        if len(sys.argv) < 3:
            print(
                'Not enough arguments. Please enter a symbol for analytics or use --help for more info.')
            quit()

        else:
            api = utils.api_connect.alpaca_connection()
            market_status = api.get_clock().is_open

            utils.analytics.analytics(sys.argv[2], market_status)

    elif (sys.argv[1] == '--market-status'):
        '''
        Check if market is open, get next open if not currently open.
        '''

        api = utils.api_connect.alpaca_connection()
        market_status = api.get_clock().is_open

        if market_status == True:
            print('The market is currently open.')
        else:
            print('The market is currently closed.')

    elif (sys.argv[1] == '--list-current-positions'):
        positions = 0
        api = utils.api_connect.alpaca_connection()
        positions = api.list_positions()

        if len(positions) == 0:
            print('You have no active positions.')
        else:
            for position in positions:
                print(position.symbol + ': ' + position.qty + ' @ $' +
                      str(round(float(position.avg_entry_price))))

    elif (sys.argv[1] == '--buy'):
        '''
        syntax ./stockli --buy [SYMBOL] [QUANTITY]
        '''

        api = utils.api_connect.alpaca_connection()

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
        '''
        syntax ./stockli --sell [SYMBOL] [QUANTITY]
        '''

        api = utils.api_connect.alpaca_connection()
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

    elif (sys.argv[1] == '--track') or (sys.argv[1] == '-t'):
        '''
        syntax ./stockli --track [SYMBOL] [PERIOD]
        '''
        api = utils.api_connect.alpaca_connection()
        market_status = api.get_clock().is_open
        # TODO: Color formatting
        # TODO: If closed, get next open
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
            trade_type = config.get_trade_type()
            print('Stockli is set to use the ' + trade_type + ' endpoint.')
        elif (sys.argv[2].lower() == 'set') and (len(sys.argv) < 4):
            print('Please specify one of the currently configured accounts.')

        elif (sys.argv[2].lower() == 'set'):
            accounts = config.list_configured_accounts()
            if not sys.argv[3].upper() in accounts:
                print(sys.argv[3] + ' is not a configured account')
            else:
                config.change_trade_type(sys.argv[3].upper())

    elif (sys.argv[1] == '--plot'):
        if (len(sys.argv) < 3):
            print('Specify symbol to be plotted.')

        from utils import plot, price_fetch
        df = price_fetch.yahoo(sys.argv[2].upper())

        plot.plot(sys.argv[2].upper(), df['Close'])
        print('Most recent close of \'' +
              sys.argv[2].upper() + '\': $' + str(df.iloc[-1]['Close']))

    else:
        print('Specified option not recognized. Do main.py -h or --help for help.')
