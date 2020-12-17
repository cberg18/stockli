from utils import ema

def macd(dataframe):
    '''
    Computes MACD
    '''
    dataframe = ema.ema(dataframe, 12)
    dataframe = ema.ema(dataframe.26)

    dataframe['MACD'] = dataframe['EMA 12'] - dataframe['EMA 26']
    dataframe = dataframe.drop(columns=['EMA 12', 'ENA 26'])
    return dataframe
