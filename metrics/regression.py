import pandas as pd
import numpy as np

# def sma(data: pd.DataFrame, **kwargs):
#     """ 
#     Returns simple moving average.
#     """
#     if("window" not in kwargs):
#         kwargs.update({"window": 20})
#     return data.rolling(**kwargs).mean()

# def ema(data: pd.DataFrame, **kwargs):
#     """ 
#     Returns exponential moving average.
#     """
#     return data.ewm(**kwargs).mean()

# def rollingStd(data: pd.DataFrame, **kwargs):
#     """ 
#     Returns rolling standard deviation.
#     """
#     if("window" not in kwargs):
#         kwargs.update({"window": 20})
#     return data.rolling(**kwargs).std()

def bollingerBands(data: pd.DataFrame, t: int = 20):
    """ 
    Uses historical price data to determine bollinger bands and moving average.
    data: pandas Dataframe containing historical price data. Requires columns "date", "high", "low", "close".
    t: Time periods used for calculating rolling statistics.

    Returns a Dataframe containing Bollinger bands (2 std.) and Moving average data points for each time period.

    See: https://www.investopedia.com/terms/b/bollingerbands.asp
    """
    data = data[["date", "high", "low", "close"]]

    bollinger = pd.DataFrame()
    bollinger["date"] = data["date"]
    bollinger["TP"] = np.true_divide((data["high"] + data["low"] + data["close"]),3)

    # bollinger["MA"] = sma(bollinger["TP"], window = t)
    bollinger["MA"] = bollinger["TP"].rolling(window = t).mean()
    # bollinger["sd"] = rollingStd(bollinger["TP"], window = t)
    bollinger["sd"] = bollinger["TP"].rolling(window = t).std()
    bollinger["-2sd"] = bollinger["MA"] - 2*bollinger["sd"]
    bollinger["-1sd"] = bollinger["MA"] - bollinger["sd"]
    bollinger["+1sd"] = bollinger["MA"] + bollinger["sd"]
    bollinger["+2sd"] = bollinger["MA"] + 2*bollinger["sd"]
    bollinger = bollinger[["date", "-2sd", "-1sd", "MA", "+1sd", "+2sd"]]
    bollinger = bollinger.set_index("date").dropna()
    return bollinger
    
def macd(data: pd.DataFrame, t: int = 9):
    """ 
    Uses historical price 
    https://www.investopedia.com/terms/b/bollingerbands.asp
    """
    data = data[["date", "close"]]
    macd = pd.DataFrame()
    macd["date"] = data["date"]
    macd["MACD"] = data["close"].ewm(span = 12, adjust = False, min_periods = 12).mean() - data["close"].ewm(span = 26, adjust = False, min_periods = 26).mean()
    macd["trigger"] = macd["MACD"].ewm(span = t, adjust = False, min_periods = t).mean()
    macd["delta"] = np.subtract(macd["MACD"], macd["trigger"])
    macd = macd.set_index("date").dropna()
    return macd