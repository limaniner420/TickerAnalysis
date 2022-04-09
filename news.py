import pandas as pd
import numpy as np
import json
from metrics import metrics, sentiment
from api.iexcloud import data
import re
import sys

ticker = sys.argv[1]
number = sys.argv[2]

# j = data.news(ticker, number)

# with open('NewsData50.json', 'w') as f:
#     json.dump(j, f)

with open('NewsData50.json') as fp:
    data = json.load(fp)

news = sentiment.sentimentAnalysis(data, number)

