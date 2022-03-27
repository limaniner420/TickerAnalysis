import pandas as pd
import numpy as np

def bollingerBands(data: pd.DataFrame, t: int = 20):
    """ 
    Uses historical price data to determine bollinger bands and moving average.
    data: pandas Dataframe containing historical price data. Requires columns "date", "high", "low", "close".
    t: Time periods used to calculating rolling statistics.

    Returns a Dataframe containing Bollinger bands (2 std.) and Moving average data points for each time period.

    See: https://www.investopedia.com/terms/b/bollingerbands.asp
    """
    data = data[["date", "high", "low", "close"]]

    bollinger = pd.DataFrame()
    bollinger["date"] = data["date"]
    bollinger["TP"] = np.true_divide((data["high"] + data["low"] + data["close"]), 3) # Typical price = (high + low + close) / 3

    bollinger["MA"] = bollinger["TP"].rolling(window = t).mean()
    bollinger["sd"] = bollinger["TP"].rolling(window = t).std()
    bollinger["-2sd"] = bollinger["MA"] - 2*bollinger["sd"]
    bollinger["-1sd"] = bollinger["MA"] - bollinger["sd"]
    bollinger["+1sd"] = bollinger["MA"] + bollinger["sd"]
    bollinger["+2sd"] = bollinger["MA"] + 2*bollinger["sd"]
    bollinger = bollinger[["date", "-2sd", "-1sd", "MA", "+1sd", "+2sd"]]
    bollinger = bollinger.set_index("date").dropna()
    return bollinger
    
def macd(data: pd.DataFrame, t_macd: int = 9, t_fast = 12, t_slow = 26):
    """ 
    Uses historical price to calculate MACD indicator.
    data: pandas Dataframe containing historical price data. Requires columns "date", "close". 
    t_macd: Time periods used to calculate MACD trigger line.
    t_fast: Time periods used to calculate fast exponential-weighted average.
    t_slow: Time periods used to calculate slow exponential-weighted average.

    Returns a Dataframe containing MACD values, trigger line and their difference.

    See: https://www.investopedia.com/terms/m/macd.asp
    """
    data = data[["date", "close"]]
    macd = pd.DataFrame()
    macd["date"] = data["date"]
    macd["MACD"] = data["close"].ewm(span = t_fast, adjust = False, min_periods = t_fast).mean() - data["close"].ewm(span = t_slow, adjust = False, min_periods = t_slow).mean()
    macd["trigger"] = macd["MACD"].ewm(span = t_macd, adjust = False, min_periods = t_macd).mean()
    macd["delta"] = np.subtract(macd["MACD"], macd["trigger"])
    macd = macd.set_index("date").dropna()
    return macd

def rsi(data: pd.DataFrame, t_periods: int = 14):
    """
    Uses historical price to calcuate the relative strength index
    data: pandas Dataframe containing historical price data. Requires columns "date", "close".
    periods: required time to calculate the rsi
    Returns a Dataframe with the relative strength index and corresponding date
    """
    delta = data['close'].diff()
    rsi = pd.DataFrame()
    rsi['date'] = data['date']
    rsi['gain'] = delta.clip(lower=0) 
    rsi['loss'] = -1*delta.clip(upper=0)
    gain_ema = rsi['gain'].ewm(com=t_periods-1, adjust=False,min_periods=t_periods).mean()
    loss_ema = rsi['loss'].ewm(com=t_periods-1, adjust=False,min_periods=t_periods).mean()
    rs = gain_ema/loss_ema

    rsi['RSI'] = 100 - (100/(1 + rs))
    #skil first 14 days
    rsi = rsi.iloc[14:]
    rsi = rsi.set_index("date").dropna()
    return rsi['RSI']
