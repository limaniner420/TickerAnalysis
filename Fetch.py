import api.iexcloud.data as api
import metrics.metrics as met
import metrics.momentum as metum
import metrics.regression as reg
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

type = input("Please input a list of type you want, if there are multiple, please seperate it with comma :")
type = re.sub(pattern, '', type)
type=  type.split(",")

try:
    j = api.batch(word,type,time)
    with open('data.json', 'w') as f:
     json.dump(j, f)
    j = api.batch(word,type,time)

except Exception as e:
    print(e)



