import pandas as pd
import numpy as np
import json
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

nltk.download('wordnet')
nltk.download('omw-1.4')

def changingSpecialChar(data):
    special_char = '@_!#$%^&*()<>?/\|}{~:;[]'

    ret = re.sub(r'[^a-zA-Z0-9$.]',' ',data)
    return ret


def sentimentAnalysis(data: pd.DataFrame, t_int: int = 50):
    """ 
    Uses intraday news data provided by iexcloud to provide a sentiment analysis on the specified stock ticker
    data: json input of News data (IEX).
    t_int: specified for amount of recent news (max/default 50)
    Ruturns an overall sentiment score by averaging all the articles.
    """

    # newsData = pd.json_normalize(data)
    newsData = data
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    newsData = newsData.drop(columns=['datetime', 'source', 'url', 'lang', 'hasPaywall', 'related', 'image'])

    newsData['headline'] = newsData['headline'].apply(lambda x: " ".join(x.lower() for x in x.split()))
    newsData['headline'] = newsData['headline'].apply(changingSpecialChar)
    newsData['headline'] = newsData['headline'].apply(lambda x: " ".join([stemmer.stem(word) for word in x.split()]))
    newsData['headline'] = newsData['headline'].apply(lambda x: " ".join([lemmatizer.lemmatize(word, pos="v") for word in x.split()]))

    newsData['summary'] = newsData['summary'].apply(lambda x: " ".join(x.lower() for x in x.split()))
    newsData['summary'] = newsData['summary'].apply(changingSpecialChar)
    newsData['summary'] = newsData['summary'].apply(lambda x: " ".join([stemmer.stem(word) for word in x.split()]))
    newsData['summary'] = newsData['summary'].apply(lambda x: " ".join([lemmatizer.lemmatize(word, pos="v") for word in x.split()]))

    file = open("metrics/negative-words.txt", 'r')
    neg_words = file.read().split()

    file = open("metrics/positive-words.txt", 'r')
    pos_words = file.read().split()
    
    newsData['total_length'] = newsData['summary'].apply(lambda x: len(re.findall(r'\w+', x))) + newsData['headline'].apply(lambda x: len(re.findall(r'\w+', x)))

    num_pos_head = newsData['headline'].map(lambda x: len([i for i in x.split() if i in pos_words]))  # i = all the words in the head/sum string
    num_pos_sum = newsData['summary'].map(lambda x: len([i for i in x.split() if i in pos_words]))
    newsData['pos_count'] = num_pos_head + num_pos_sum

    num_neg_head = newsData['headline'].map(lambda x: len([i for i in x.split() if i in neg_words]))
    num_neg_sum = newsData['summary'].map(lambda x: len([i for i in x.split() if i in neg_words]))
    newsData['neg_count'] = num_neg_head + num_neg_sum

    newsData['sentiment'] = round((newsData['pos_count'] - newsData['neg_count']) / newsData['total_length'], 3)
    #print(newsData['pos_count'].count(),newsData['neg_count'].count())

    meanSentiment = round(newsData['sentiment'].mean(), 3)
    # print("The mean sentiment of this ticker is :", meanSentiment)

    # newsData.to_csv("newsDataOutput") #to get output of sentiment analysis 

    return newsData, meanSentiment
