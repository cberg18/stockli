import pandas as pd
import yfinance as yf


def yahoo(sym,period='max'):
    symbol = yf.Ticker(sym)
    hist = symbol.history(period='max')
    return hist
