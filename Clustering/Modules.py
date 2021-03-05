"""
This script contains functions for tokenisation, stemming and removing stop words
used as preprocessing for the clustering process.
"""

import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
import json


def Tokenize(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


def Stemming(text):
    x = 1
    return x


def remove_stops(text, stopwords):
    x = 1
    return x


#%% #Testing the modules
with open('copernicus_scrape/ADS_data.json') as f:
  text = json.load(f)
  
text_string = []
N = len(text)
for i in range(N):
    tmp = json.dumps(text[i])
    text_string.append(tmp)

#nltk.download() # run to download nltk dependencies

#Tokenisation
tokenised = Tokenize(text_string[0])    

# stemming
stemmer = nltk.stem.snowball.SnowballStemmer("english")

#Remove stopwords
stopwords = nltk.corpus.stopwords.words('english')
#print(stopwords[:10])

