from numpy.lib.function_base import append
from utils import price_fetch
import pandas_ta as ta


def analytics(symbol,market_status):
    symHistory = price_fetch.yahoo(symbol)
    symHistory.ta.rsi(append=True)
    symHistory.ta.sma(length=20, append=True)
    symHistory.ta.sma(length=50, append=True)
    symHistory.ta.sma(length=100, append=True)
    symHistory.ta.sma(length=200, append=True)
    symHistory.ta.rsi(append=True)
    symHistory.ta.willr(append=True)
    todays_volume = symHistory['volume'].iloc[-1]
    last_close = symHistory['close'].iloc[-1]

    print('Report for: ' + symbol.upper())
    if market_status == False:
        print('Last market close: $%2.2f' %(last_close) )
    if market_status == True:
        print('Most recent price: $%2.2f' %(last_close) )
    
