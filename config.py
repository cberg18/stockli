# TODO: function for initializing config
# TODO: function for validating config

from configparser import ConfigParser

config_object = ConfigParser()

config_object.read('config.ini')


'''
The following section is temproary and only to 
make the main program work until I can build proper
config handling.
'''
method = config_object['TRADE_METHOD']['trade_method']


if method == 'paper':
    API_KEY = config_object['PAPER']['PAPER_API_KEY']
    API_SECRET = config_object['PAPER']['PAPER_API_SECRET']
    BASE_URL = config_object['PAPER']['PAPER_BASE_URL']

elif method == 'live':
    API_KEY = config_object['LIVE']['LIVE_API_KEY']
    API_SECRET = config_object['LIVE']['LIVE_API_SECRET']
    BASE_URL = config_object['LIVE']['LIVE_BASE_URL']


def load_config():
    """
    This function loads the config.
    """
    config_object = ConfigParser()
    config_object.read('config.ini')
    return config_object


def list_configured_accounts():
    """
    This function lists configured accounts.
    """
    load_config()
    for i in config_object:
        print(i)

    pass


def add_account_details(account_name, api_key, api_secret, base_url):
    """
    This function provides functionality for adding account details.
    """
    config_object[account_name.upper()] = {
        'API_KEY': api_key,
        'API_SECRET': api_secret,
        'BASE_URL': base_url
    }

    with open('config.ini', 'w') as conf:
        config_object.write(conf)
    pass


def remove_account_details(account_name):
    """
    This function provides functionality for removing account details.
    """
    pass


def modify_account_details(parameter_list):
    """
    This function provides functionality for modifying currently configured accounts.
    """
    pass
