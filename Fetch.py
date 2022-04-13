import api.iexcloud.data as api
import metrics.metrics as met
import metrics.momentum as metum
import json
import pandas as pd
import re

j = api.hist_price("AAPL","3m")
j = pd.json_normalize(j)
pattern = re.compile(r'\s+')
word = input("Please input a list stock symbol, if there are multiple, please seperate it with comma :")
word = re.sub(pattern, '', word)
word=  word.split(",")
time = input("Plase input the time range: ")

try:
    j = api.batch(word,["chart"],time,mode = "cloud")
    with open('data.json', 'w') as f:
     json.dump(j, f)
    for x in word:
        k = api.news(x, "20")
        with open( x + '.json', 'w') as f:
            json.dump(k, f)        
except Exception as e:
    print(e)



