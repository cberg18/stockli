def rsi(dataframe):
    '''
    Calculates the RSI for a stock.
    '''
    dataframe['Delta']= dataframe['Close']-dataframe['Close'].shift(1)
    dataframe['U']=dataframe['Delta'].where(dataframe['Delta']>0).fillna(0).rolling(14).mean()
    dataframe['D']=dataframe['Delta'].where(dataframe['Delta']<0).fillna(0).rolling(14).mean().abs()

    #calculate rs
    dataframe['RS'] = dataframe['U']/dataframe['D']
    #caluclate rsi
    dataframe['RSI']=(100-(100/((dataframe['RS']+1))))
    #drop extra columns
    dataframe = dataframe.drop(columns=['U','D','Delta','RS'])
    return dataframe
