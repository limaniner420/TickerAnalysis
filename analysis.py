import api.iexcloud.data as api
import metrics.metrics as met
import metrics.momentum as metum
import json
import pandas as pd
import re
from datetime import datetime
from metrics import sentiment
import matplotlib.pyplot as plt

    
word = input("Please input a stock symbol which you want to analysis :")
try:
    file = pd.read_json("data.json")
    data = pd.DataFrame(file[word]['chart'])    
    weight = 0
    news_data = pd.DataFrame(file[word]['news'])  
except Exception as e:
    print("The stock data haven't fetched, please fetch first in the fetch.py")
    exit()
price = data.iloc[-1]['close']
# print(data)

#bolli
bolli = metum.bollingerBands(data)
d2 = bolli.iloc[-1]
bo_val = 0

if(price >= d2["+2sd"]):
    bo_val += 1
    print("\nBBands score :",bo_val,"(buy)")
elif (price >= d2["+1sd"]):
    bo_val += 0.5
    print("\nBBands score :",bo_val,"(buy)")
elif (price >= d2["-1sd"]):
    bo_val += 0
    print("\nBBands score :",bo_val,"(hold)")
elif (price >= d2["+1sd"]):
    bo_val -= 0.1
    print("\nBBands score :",bo_val,"(sell)")
else:
    bo_val -= 0.5
    print("\nBBands score :",bo_val,"(sell)")
# print(d2)

#macd
macd = metum.macd(data)
delta = macd.iloc[-1]["delta"]
macd_val = 0
if(abs(delta) <= 0.05):
    macd_val += 0
    print("MACD score :",macd_val,"(hold)")
elif(delta > 0 ):
    macd_val += 1
    print("MACD score :",macd_val,"(buy)")
else:
    macd_val -= 1
    print("MACD score :",macd_val,"(sell)")
# print(macd.iloc[-1])


#rsi
rsi = metum.rsi(data)
rsi_val = 0
if(rsi.iloc[-1]['RSI']>= 30 and rsi.iloc[-1]['RSI'] <= 70):
    rsi_val += 0
    print("RSI score :",rsi_val,"(hold)")
elif( rsi.iloc[-1]['RSI'] < 30):
    rsi_val += 1
    print("RSI score :",rsi_val,"(buy)")
else:
    rsi_val -= 1
    print("RSI score :",rsi_val,"(sell)")
# print(rsi.iloc[-1])

#Stochastic
Stoc = metum.Stochastic(data)
stoc_val = 0
if(Stoc.iloc[-1]['K'] > 80 and Stoc.iloc[-1]['D'] > 80 and Stoc.iloc[-1]['D'] > Stoc.iloc[-1]['D']):
    stoc_val -= 1
    print("KD score :",stoc_val,"(sell)")
elif(Stoc.iloc[-1]['K'] < 20 and Stoc.iloc[-1]['D'] < 20 and Stoc.iloc[-1]['K'] > Stoc.iloc[-1]['D']):
    stoc_val += 1
    print("KD score :",stoc_val,"(buy)")
else:
    stoc_val = 0
    print("KD score :",stoc_val,"(hold)")
# print(Stoc.iloc[-1])

#sentiment
news,number2 = sentiment.sentimentAnalysis(news_data, '10')
news_val = 0
if(number2 >= 0):
    news_val += 1
    print("Sentiment score :",news_val,"(buy)")
else:
    news_val -= 1
    print("Sentiment score :",news_val,"(sell)")


#Grade
weight = (bo_val + macd_val + rsi_val + stoc_val+ news_val)/5 

#graphing 
fig, (price, Rsi,kd) = plt.subplots(3)
fig.set_size_inches(18.5, 10.5)
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
kd.set_ylabel('Stochastic oscillator')

if(abs(weight) <= 0.1):
    print("\nOverall rating :",weight, "(hold)" )
elif(weight > 0):
    print("\nOverall rating :",weight, "(buy)" )
else:
    print("\nOverall rating :",weight, "(sell)" )


plt.show()
