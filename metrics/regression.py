import pandas as pd
import numpy as np

def movingAverage(data: pd.DataFrame, t: int = 20):
    return data.rolling(t).mean()

def rollingStd(data: pd.DataFrame, t: int = 20):
    return data.rolling(t).std()

def bollingerBands(data: pd.DataFrame, t: int = 20):
    """ 
    Uses historical price data to determine bollinger bands and moving average.
    data: pandas Dataframe containing historical price data. Requires columns "date", "high", "low", "close".
    t: Time periods used for calculating rolling statistics.

    Returns a Dataframe containing Bollinger bands (2 std.) and Moving average data points for each time period.
    """
    data = data[["date", "high", "low", "close"]]
    data["TP"] = np.true_divide((data["high"] + data["low"] + data["close"]),3)
    data = data[["date", "TP"]]
    # data.set_index("date")

    bollinger = pd.DataFrame()
    bollinger["date"] = data["date"]
    bollinger["MA"] = movingAverage(data["TP"], t = t)
    bollinger["sd"] = rollingStd(data["TP"], t = t)
    bollinger["-2sd"] = bollinger["MA"] - 2*bollinger["sd"]
    bollinger["-1sd"] = bollinger["MA"] - bollinger["sd"]
    bollinger["+1sd"] = bollinger["MA"] + bollinger["sd"]
    bollinger["+2sd"] = bollinger["MA"] + 2*bollinger["sd"]
    bollinger = bollinger[["date", "-2sd", "-1sd", "MA", "+1sd", "+2sd"]]
    bollinger = bollinger.dropna()
    bollinger = bollinger.set_index("date")
    return bollinger
    