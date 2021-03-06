"""
This script contains functions for tokenisation, stemming and removing stop words
used as preprocessing for the clustering process.
"""


import nltk
import re
import json


def Tokenize(text):
    """
    Seperates a sentence into tokens

    Parameters
    ----------
    text : string
        Sentence to by tokenized 

    Returns
    -------
    filtered_tokens : list
        Contains a token in each entrance.

    """
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


def Stemming(tokens, stemmer = nltk.stem.snowball.SnowballStemmer("english")):
    """
    Stems words

    Parameters
    ----------
    tokens : list of strings containing a single word
        Strings to be stemmed 

    stemmer : nltk object
        Stemming technique
        
    Returns
    -------
    stems : list
        Contains a stemmed token in each entrance.

    """
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def remove_stops(stems, stopwords, amount = 179):
    """
    Removes Stopwords

    Parameters
    ----------
    stems : list of strings containing a single stemmed word
        Strings with words which might be deleted 

    stopwords : list of stopwods
        The words which are unwanted
    
    amount : interger
         the amount of stopwords to be removed   
    Returns
    -------
    filtered_sentence : list
        Containing no stop words.

    """
    filtered_sentence = [w for w in stems if not w in stopwords[:amount]] 
    return filtered_sentence


#%% #Testing the modules
with open('copernicus_scrape/ADS_data.json') as f:
  text = json.load(f)
  
text_string = []
N = len(text)
for i in range(N):
    tmp = json.dumps(text[i])
    text_string.append(tmp)

# nltk.download() # run to download nltk dependencies

# Tokenisation
tokens = Tokenize(text_string[0])    
print(tokens)

# Stemming
stemmer = nltk.stem.snowball.SnowballStemmer("english")
stems = Stemming(tokens, stemmer = stemmer)
print(stems) # for instance look at entrace 9, 10, 11 or 12

# Remove stopwords
stopwords = nltk.corpus.stopwords.words('english')
no_stops = remove_stops(stems, stopwords, amount = 179) # for instance look at entrace 18 or 19 compared to stems
print(no_stops)
