from numpy.lib.function_base import append
from utils import price_fetch
import pandas_ta as ta


def analytics(symbol, market_status):
    symHistory = price_fetch.yahoo(symbol)
    rsi = symHistory.ta.rsi(append=True).iloc[-1]
    sma_20 = symHistory.ta.sma(length=20, append=True).iloc[-1]
    sma_50 = symHistory.ta.sma(length=50, append=True).iloc[-1]
    sma_100 = symHistory.ta.sma(length=100, append=True).iloc[-1]
    sma_200 = symHistory.ta.sma(length=200, append=True).iloc[-1]
    willr = symHistory.ta.willr(append=True).iloc[-1]
    bbl = symHistory.ta.bbands()['BBL_5_2.0'].iloc[-1]
    bbm = symHistory.ta.bbands()['BBM_5_2.0'].iloc[-1]
    bbu = symHistory.ta.bbands()['BBU_5_2.0'].iloc[-1]
    todays_volume = symHistory['volume'].iloc[-1]
    last_close = symHistory['close'].iloc[-1]

    symHistory = symHistory.drop(columns=['Dividends', 'Stock Splits'])
    print('Report for: ' + symbol.upper())
    print('Data from ' + str(symHistory.tail(1).index[0])[:10])

    if market_status == False:
        print('Last market close: $%2.2f' % (last_close))
    if market_status == True:
        print('Most recent price: $%2.2f' % (last_close))

    '''for col in symHistory.columns:
        print(col)
        print(symHistory[col].iloc[-1])'''

    print('Volume: %d   ' % (todays_volume))
    print('SMA 20: %5.2f SMA 50: %5.2f    SMA 100: %5.2F   SMA 200: %5.2F' %
          (sma_20, sma_50, sma_100, sma_200))
    print('RSI: %3.2f    Will. R: %3.2f' % (rsi, willr))
    print('BBL: %5.2f    BBM: %5.2f       BBU: %5.2f' % (bbl, bbm, bbu))
