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


def sentimentAnalysis(data: json, t_int: int = 50):
    """ 
    data: json input of News data (IEX).
    t_int: specified for amount of recent news
    returns a sentiment score gathered from analyzing recent news
    """


    hist = pd.json_normalize(data)
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    hist = hist.drop(columns=['datetime', 'source', 'url', 'lang', 'hasPaywall', 'related', 'image'])

    hist['headline'] = hist['headline'].apply(lambda x: " ".join(x.lower() for x in x.split()))
    hist['headline'] = hist['headline'].apply(changingSpecialChar)
    hist['headline'] = hist['headline'].apply(lambda x: " ".join([stemmer.stem(word) for word in x.split()]))
    hist['headline'] = hist['headline'].apply(lambda x: " ".join([lemmatizer.lemmatize(word, pos="v") for word in x.split()]))

    hist['summary'] = hist['summary'].apply(lambda x: " ".join(x.lower() for x in x.split()))
    hist['summary'] = hist['summary'].apply(changingSpecialChar)
    hist['summary'] = hist['summary'].apply(lambda x: " ".join([stemmer.stem(word) for word in x.split()]))
    hist['summary'] = hist['summary'].apply(lambda x: " ".join([lemmatizer.lemmatize(word, pos="v") for word in x.split()]))

    file = open("metrics/negative-words.txt", 'r')
    neg_words = file.read().split()

    file = open("metrics/positive-words.txt", 'r')
    pos_words = file.read().split()
    
    hist['total_length'] = hist['summary'].apply(lambda x: len(re.findall(r'\w+', x))) + hist['headline'].apply(lambda x: len(re.findall(r'\w+', x)))

    num_pos_head = hist['headline'].map(lambda x: len([i for i in x.split() if i in pos_words]))  # i = all the words in the head/sum string
    num_pos_sum = hist['summary'].map(lambda x: len([i for i in x.split() if i in pos_words]))
    hist['pos_count'] = num_pos_head + num_pos_sum

    num_neg_head = hist['headline'].map(lambda x: len([i for i in x.split() if i in neg_words]))
    num_neg_sum = hist['summary'].map(lambda x: len([i for i in x.split() if i in neg_words]))
    hist['neg_count'] = num_neg_head + num_neg_sum

    hist['sentiment'] = round((hist['pos_count'] - hist['neg_count']) / hist['total_length'], 3)

    meanSentiment = round(hist['sentiment'].mean(), 3)
    print("The mean sentiment of this ticker is :", meanSentiment)

    hist.to_csv("HistOutput") #remove later

    #rmb to write docstrings for your fs

    return hist