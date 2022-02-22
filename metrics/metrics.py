import pandas as pd
import numpy as np
import json
import statsmodels.nonparametric.smoothers_lowess as st_lowess

def movAvg(data: json, t_long: int = 50, t_short: int = 200):
    if t_long < 1 or t_short < 1 or t_long <= t_short:
        return None

    hist = pd.json_normalize(data)
    hist["date"] = pd.to_datetime(hist["date"])
    hist_long_ma = np.mean(hist[-t_long:]["close"])
    hist_short_ma = np.mean(hist[-t_short:]["close"])
    return (hist_short_ma - hist_long_ma) / hist_short_ma

def meanRev(data: json, t: int, range: int = 24):
    hist = data[-t:]
    hist = pd.json_normalize(data)
    hist["date"] = pd.to_datetime(hist["date"])
    hist_lowess = st_lowess.lowess(hist["close"], hist["date"], frac = range / len(hist["date"]), is_sorted = True)
    delta = (hist.iloc[-1]["close"] - hist_lowess[-1][1]) / hist_lowess[-1][1]
    return delta