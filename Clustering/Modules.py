"""
This script contains functions for tokenisation, stemming and removing stop words
used as preprocessing for the clustering process.
"""


import nltk
import re
import json
import numpy as np


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


def remove_stops(stems, stopwords = nltk.corpus.stopwords.words('english'), amount = 179):
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


def Preprocessing(text, stemmer = nltk.stem.snowball.SnowballStemmer("english"), stopwords = nltk.corpus.stopwords.words('english')):
    """
    Tokenizes, stems and removes stop words from sentences

    Parameters
    ----------
    text : list
        list containing string with the sentences to be preprocessed.
        
    stemmer : nltk object
        Stemming technique
    
    stopwords : list of stopwods
        The words which are unwanted

    Returns
    -------
    TYPE list
        Preprocessed sentences.

    """
    tokens = [Tokenize(text[i]) for i in range(len(text))]
    stems = [Stemming(tokens[i], stemmer = stemmer) for i in range(len(tokens))]
    no_stops = [remove_stops(stems[i], stopwords, amount = 179) for i in range(len(stems))]
    return no_stops

def jaccard_distance(list1, list2):
    """
    Computes the jaccard distance between to lists. The lists
    are converted to sets, i.e., order and duplicates in the lists are
    removed.

    Parameters
    ----------
    list1 : list
        The first list.
    list2 : list
        The second list.

    Returns
    -------
    TYPE float
        The jaccard distance.

    """
    
    set1 = set(list1)
    set2 = set(list2)
    cap = len(set1.intersection(set2))
    return 1 - cap/(len(set1) + len(set2) - cap)


def jaccard_matrix(documents):
    """
    Computes the jaccard distance between all input documents. 

    Parameters
    ----------
    documents : list of lists.
        The documents for which the jaccard distance should be calculated. 
        Let the number of documents be N.

    Returns
    -------
    jac_mat : ndarray, size (N,N,)
        Symmetric matrix. Index i,j contains the jaccard distance between 
        documents i and j.

    """
    
    N = len(documents)
    jac_mat = np.zeros((N,N))
    for i in range(N-1):
        for j in range(i+1,N):
            jac_mat[i,j] = jaccard_distance(documents[i], documents[j])
            jac_mat[j,i] = jac_mat[i,j]
            
    return jac_mat


def jaccard_matrix_update(old_matrix, old_documents, new_documents):
    """
    Compute and insert Jaccard distance from new docutments in the Jaccard 
    matrix.

    Parameters
    ----------
    old_matrix : ndarray, size (N,N,)
        The old Jaccard matrix.
    old_documents : list of lists
        The list of documents already represented in the Jaccard matrix.
        Let the number of documents be N.
    new_documents : list of lists
        The new documents for which the jaccard distance should be calculated. 
        Let the number of documents be M.

    Returns
    -------
    jac_mat : ndarray, size (N+M,N+M,)
        Updated Jaccard matrix.

    """
    
    M = len(new_documents)
    N = old_matrix.shape[0]
    jac_mat = np.zeros((N+M,N+M))
    jac_mat[:N,:N] = old_matrix
    for i in range(N):
        for j in range(M):
            jac_mat[i,N+j] = jaccard_distance(old_documents[i], new_documents[j])
            jac_mat[N+j,i] = jac_mat[i,N+j]
    
    jac_mat[N:,N:] = jaccard_matrix(new_documents)
    return jac_mat

def nearest_10(documents, jaccard_mat, doc_num):
    """
    Returns a list of dictionaries containing 10 closest websites in terms 
    of Jaccard distance and the jaccard distance to the docucment specified 
    by doc_num in the list of documents.

    Parameters
    ----------
    documents : list of dicts
        List of all the documents in dict format.
    jaccard_mat : ndarray 
        The Jaccard matrix.
    doc_num : int
        The index of the document which we want to find the 10 nearest documents for.

    Returns
    -------
    docs : list of dicts
        List of dicts containing the 10 nearest documents and the Jaccard distance.

    """
    choose_docs = np.concatenate((jaccard_mat[doc_num,:doc_num], jaccard_mat[doc_num,doc_num+1:]))
    print(choose_docs)
    indeces = np.argsort(choose_docs)[:10]
    docs = [{"Webpage": documents[indeces[i]].get("Webpage"), "score": jaccard_mat[doc_num, indeces[i]]} for i in range(10)]
    return docs


#%% #Testing the modules
with open('copernicus_scrape/CDS_data.json') as f:
  text = json.load(f)
  
text_string = []
N = len(text)
for i in range(N):
    tmp = json.dumps(text[i])
    text_string.append(tmp)

# nltk.download() # run to download nltk dependencies.

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

# Compute jaccard matrix

tokens = [Tokenize(text_string[i]) for i in range(len(text_string))]
stems = [Stemming(tokens[i], stemmer = stemmer) for i in range(len(tokens))]
no_stops = [remove_stops(stems[i], stopwords, amount = 179) for i in range(len(stems))]
jaccard_mat = jaccard_matrix(no_stops)

near = nearest_10(text, jaccard_mat, 95)

no_stops = Preprocessing(text_string, stemmer = stemmer, stopwords = stopwords)
jaccard_mat = jaccard_matrix(no_stops)

