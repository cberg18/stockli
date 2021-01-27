from utils import price_fetch

class Symbol:
    def __init__(self,symbol):
        self.name = symbol
        self.symHistory = price_fetch.yahoo(symbol)
        self.lastClose = self.symHistory['Close'].iloc[-1]
