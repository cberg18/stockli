def sma(dataframe, window):
    '''
    Calculate sma for a given period.
    '''
    name = 'SMA ' + str(window)

    dataframe[name] = dataframe['Close'].rolling(window).mean().round(2)
    return dataframe
