import pandas as pd
import numpy as np
import json
from metrics import metrics, sentiment
from api.iexcloud import data
import re



# j = data.news("AAPL", "50")

# with open('Newsdata50.json', 'w') as f:
#     json.dump(j, f)

with open('Newsdata50.json') as fp:
    data = json.load(fp)

news = sentiment.sentimentAnalysis(data)

#find out how many times a keyword is used (good vs bad) //count make a dictionary with keyword 
