import pandas as pd
import numpy as np
import json
from metrics import metrics 
from api.iexcloud import data

j = data.news("AAPL", "10")

with open('data.json', 'w') as f:
    json.dump(j, f)

hist = pd.json_normalize(j)
print(hist) #added for test


