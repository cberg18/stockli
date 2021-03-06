# TODO: function for initializing config
# TODO: function for validating config

from configparser import ConfigParser

config_object = ConfigParser()

config_object.read('config.ini')


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
    config_object = load_config()
    accounts = []
    for i in config_object:
        if i == 'DEFAULT' or i == 'TRADE_METHOD':
            continue
        else:
            accounts.append(i)
    return accounts


def get_trade_type():
    config_object = load_config()
    return config_object['TRADE_METHOD']['trade_method']


def add_account_details(account_name, api_key, api_secret, base_url):
    """
    This function provides functionality for adding account details.
    """
    config_object = load_config()
    if account_name.upper() in config_object:
        print(account_name +
              'already exists in config.ini, please chose a different name.')
    else:
        config_object[account_name.upper()] = {
            'API_KEY': api_key,
            'API_SECRET': api_secret,
            'BASE_URL': base_url
        }

        with open('config.ini', 'w') as conf:
            config_object.write(conf)
        print(account_name.upper() + ' has been configured. ')


def remove_account_details(account_name):
    """
    This function provides functionality for removing account details.
    """
    config_object = load_config()
    if not account_name in config_object:
        print(account_name +
              'does not exist in the config, are you sure the account name is correct?')
    elif account_name in config_object:
        config_object.remove_section(account_name)
        with open('config.ini', 'w') as conf:
            config_object.write(conf)

        print(account_name + ' successfully removed.')


def load_keys():
    config_object = load_config()
    trade_method = config_object['TRADE_METHOD']['trade_method']

    if trade_method == 'paper':
        API_KEY = config_object['PAPER']['API_KEY']
        API_SECRET = config_object['PAPER']['API_SECRET']
        BASE_URL = config_object['PAPER']['BASE_URL']

        return (API_KEY, API_SECRET, BASE_URL)

    if trade_method == 'live':
        API_KEY = config_object['LIVE']['API_KEY']
        API_SECRET = config_object['LIVE']['API_SECRET']
        BASE_URL = config_object['LIVE']['BASE_URL']

        return (API_KEY, API_SECRET, BASE_URL)


def modify_account_details(parameter_list):
    # TODO: build this function
    """
    This function provides functionality for modifying currently configured accounts.
    """
    pass


def change_trade_type(trade_type):
    '''
    This function modifies the currently set trade type.
    '''
    config_object = load_config()
    config_object.set('TRADE_METHOD', 'trade_method', trade_type)

    with open('config.ini', 'w') as conf:
        config_object.write(conf)
    print('Trading type has been set to ' + trade_type.upper())
