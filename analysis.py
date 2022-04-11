import api.iexcloud.data as api
import metrics.metrics as met
import metrics.momentum as metum
import metrics.regression as reg
import json
import pandas as pd
import re
from datetime import datetime
import matplotlib.pyplot as plt

    
word = input("Please input a stock symbol which you want to analysis :")

try:
    file = pd.read_json("data.json")
    data = pd.DataFrame(file[word]['chart'])    
    weight = 0
except Exception as e:
    print("the stock data haven't fetched, please fetch first in the fetch.py")
    exit()

price = data.iloc[-1]['close']

#bolli
bolli = metum.bollingerBands(data)
d2 = bolli.iloc[-1]
if(price >= d2["+2sd"]):
    weight += 1
elif (price >= d2["+1sd"]):
    weight += 0.5
elif (price >= d2["-1sd"]):
    weight += 0
elif (price >= d2["+1sd"]):
    weight -= 0.5
else:
    weight -= 1


#macd
macd = metum.macd(data)
mval = macd.iloc[-1]["MACD"]
if(mval == 0):
    weight += 0
elif(mval > 0 ):
    weight += 0.5
else:
    weight -= 0.5

print(macd)

#rsi
rsi = metum.rsi(data)
mean = rsi['RSI'].rolling(len(rsi)).mean().iloc[-1]
if(rsi.iloc[-1]['RSI'] == mean or (rsi.iloc[-1]['RSI']>= 30 and rsi.iloc[-1]['RSI'] <= 70)):
    weight += 0
elif(rsi.iloc[-1]['RSI'] <= mean or rsi.iloc[-1]['RSI'] < 30):
    weight += 0.5
else:
    weight -= 0.5



plt.show()


#Stochastic
Stoc = metum.Stochastic(data)
if(Stoc.iloc[-1]['K'] > 80 and Stoc.iloc[-1]['d'] > 80 and Stoc.iloc[-1]['d'] > Stoc.iloc[-1]['k']):
    weight -= 1
elif(Stoc.iloc[-1]['K'] < 20 and Stoc.iloc[-1]['d'] < 20 and Stoc.iloc[-1]['k'] > Stoc.iloc[-1]['d']):
    weight += 1


#graphing 
fig, (price, Rsi,kd) = plt.subplots(3)
fig.suptitle(word)
price_data = data[['date','close']]
price_data = price_data.set_index("date").dropna()
price_data['close'].plot(ax=price)
price.set_ylabel('Price')
rsi['RSI'].plot(ax=Rsi)
Rsi.set_ylim(0,100)
Rsi.axhline(30, color='r', linestyle='--')
Rsi.axhline(70, color='r', linestyle='--')
Rsi.set_ylabel('RSI')
Stoc[['K', 'D']].plot(ax=kd)
kd.set_ylim(0,100)
kd.axhline(20, linestyle='--', color="r")
kd.axhline(80, linestyle="--", color="r")
plt.show()


if(weight > 0):
    print("After different analysis, it is a good timing to buy this stock if you are considering when to buy it")
else:
    print("After different analysis, it is not a good timing to buy this stock, you might consider to sell or hold it")
