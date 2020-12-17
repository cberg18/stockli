def ema(dataframe, window):
    '''
    Calculates exponential moving average.
    '''
    name = 'EMA ' + str(window)

    dataframe[name] = dataframe['Close'].ewm(span=window).mean().round(2)
    return dataframe
