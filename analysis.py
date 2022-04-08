import api.iexcloud.data as api
import metrics.metrics as met
import metrics.momentum as metum
import metrics.regression as reg
import json
import pandas as pd
import re

    
word = input("Please input a stock symbol which you want to analysis :")
file = pd.read_json("data.json")
data = pd.DataFrame(file[word]['chart'])
weight = 0
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

print(weight)

#macd
macd = metum.macd(data)
mval = macd.iloc[-1]["MACD"]
if(mval == 0):
    weight += 0
elif(mval > 0 ):
    weight += 0.5
else:
    weight -= 0.5

print(weight)



#rsi
rsi = metum.rsi(data)
print(rsi)
mean = rsi['RSI'].rolling(len(rsi)).mean().iloc[-1]
if(rsi.iloc[-1]['RSI'] == mean):
    weight += 0
elif(rsi.iloc[-1]['RSI'] >= mean):
    weight += 0.5
else:
    weight -= 0.5


print(weight)

#volatility
#volat = metum.volatility(data)
#print(volat)

#Stochastic
Stoc = metum.Stochastic(data)
#print(Stoc)

