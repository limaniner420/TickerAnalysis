import pandas as pd
import numpy as np
import json
import statsmodels.nonparametric.smoothers_lowess as st_lowess

def movAvgDiff(data: json, t_long: int = 200, t_short: int = 50, normalised: bool = True):
    """ 
    data: json input of historical price data (IEX).
    t: time periods specified for comparison of moving avgs. t_long must be greater than t_short for valid data.
    normalised:
        true: returns fractional difference.
        false: returns absolute difference.
    returns difference in moving average.
    """

    if t_long < 1 or t_short < 1 or t_long <= t_short:
        return None

    hist = pd.json_normalize(data)
    hist["date"] = pd.to_datetime(hist["date"])
    hist_long_ma = np.mean(hist[-t_long:]["close"])
    hist_short_ma = np.mean(hist[-t_short:]["close"])
    return (hist_short_ma - hist_long_ma) / (hist_long_ma if normalised else 1)

def meanRev(data: json, t_data: int = None, t_ma: int = 24):
    """ 
    data: json input of historical price data (IEX).
    t_data: specify length of time for comparison.
    t_ma: specify no. of data points used for lowess.
    returns difference of current price to lowess regression.
    """

    if (t_data != None):
        hist = data[-t_data:]
    else:
        hist = data
        
    hist = pd.json_normalize(data)
    hist["date"] = pd.to_datetime(hist["date"])
    hist_lowess = st_lowess.lowess(hist["close"], hist["date"], frac = t_ma / len(hist["date"]), is_sorted = True)
    delta = (hist.iloc[-1]["close"] - hist_lowess[-1][1]) / hist_lowess[-1][1]
    return delta