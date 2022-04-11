import pandas as pd

def movingAverage(data: pd.DataFrame, t_long: int = 200, t_short: int = 50) -> pd.DataFrame:
    """ 
    data: pandas Dataframe containing historical price data. Requires columns "date", "close". 
    t: Time periods used to calculate moving averages. T_long must be greater than t_short for valid data.
    
    Returns Dataframe containing fast and slow moving averages.

    See: https://www.investopedia.com/terms/c/crossover.asp
    """

    # TODO: validity check.
    ma = pd.DataFrame()
    ma["date"] = data["date"]
    ma["ma_long"] = data["close"].rolling(window = t_long).mean()
    ma["ma_short"] = data["close"].rolling(window = t_short).mean()
    ma = ma.set_index("date").dropna()
    return ma

def fiboRetracement(data: pd.DataFrame, t: int = 365):
    """ 
    data: pandas Dataframe containing historical price data. Requires column "close". 
    t: Time periods used to calculate extremas.
    
    Returns Dataframe containing Fibonacci retracement levels.

    See: https://www.investopedia.com/articles/active-trading/091114/strategies-trading-fibonacci-retracements.asp
    """
    temp = data[["close"]][-t:]
    fib = pd.DataFrame()

    min = temp["close"].min()
    max = temp["close"].max()
    delta = max - min

    fib["0%"] = min
    fib["23.6%"] = 0.236 * delta + min
    fib["38.2%"] = 0.382 * delta + min
    fib["50.0%"] = 0.5 * delta + min
    fib["61.8%"] = 0.618 * delta + min
    fib["76.4%"] = 0.764 * delta + min
    fib["100%"] = max
    return fib