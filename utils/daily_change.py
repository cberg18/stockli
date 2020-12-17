def daily_change(dataframe):
    '''
    Calculates the daily % change for a stock.
    '''
    dataframe['Change'] = ((dataframe['Open'] - dataframe['Close']) / dataframe['Open']) * 100
    dataframe['Change'] = dataframe['Change'].round(2)
    return dataframe
