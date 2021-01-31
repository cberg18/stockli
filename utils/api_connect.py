import alpaca_trade_api as tradeapi

try:
    import config
except ModuleNotFoundError:
    print('The config file seems to be missing.')
    print('Use ./stockli.py --config for help setting up the config file.')
    quit()


def alpaca_connection():
    trading_type = 'paper'

    API_KEY = config.API_KEY
    API_SECRET = config.API_SECRET
    BASE_URL = config.BASE_URL

    # initialize connection to api and get market status
    api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL)
    return api
