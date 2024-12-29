def calculate_moving_average(data, period = 14):
    return data.ewm(span=period, adjust=False).mean()

def calculateAverageTrueRange(data): 
    tr = data.diff().abs()
    atr = tr.rolling(window=14).mean()
    
    return atr
