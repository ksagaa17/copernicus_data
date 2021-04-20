# -*- coding: utf-8 -*-
"""
Jaccard example
"""

import numpy as np
from sklearn.metrics import jaccard_score


doc1 = ['my', 'name', 'is', 'johannes']
doc2 = ['my', 'name', 'is', 'ulla']
doc3 = ['johannes', 'is', 'my', 'name']
doc4 = ['my', 'name', 'is', 'johannes', 'is', 'my', 'eeh']
doc5 = ['der', 'var', 'engang', 'hejsa', 'is', 'ulla']
doc6 = ['say', 'my', 'name', 'you', 'are', 'ulla']
# doc4 = doc1

# print('average: micro')
# for doc in [doc1, doc2, doc3, doc4]:
#     score = jaccard_score(doc1, doc, average='micro') 
#     print(score)
    
# print('average: macro')
# for doc in [doc1, doc2, doc3, doc4]:
#     score = jaccard_score(doc1, doc, average='macro') 
#     print(score)

# print('average: weighted')
# for doc in [doc1, doc2, doc3, doc4]:
#     score = jaccard_score(doc1, doc, average='weighted') 
#     print(score)

# print('average: None')
# for doc in [doc1, doc2, doc3, doc4]:
#     score = jaccard_score(doc1, doc, average=None) 
#     print(score)


# average samples and binary does not work with this example


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
    #cup = len(set(list1).union(set(list2)))
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
            print('{},{}'.format(i,j))
            jac_mat[j,i] = jac_mat[i,j]
            
    return jac_mat

def jaccard_matrix_update(old_matrix, old_documents, new_documents):
    M = len(new_documents)
    N = old_matrix.shape[0]
    jac_mat = np.zeros((N+M,N+M))
    jac_mat[:N,:N] = old_matrix
    print(jac_mat)
    for i in range(N):
        for j in range(M):
            jac_mat[i,N+j] = jaccard_distance(old_documents[i], new_documents[j])
            print('{},{}'.format(i,j))
            jac_mat[N+j,i] = jac_mat[i,N+j]
    
    print(jac_mat)
    jac_mat[N:,N:] = jaccard_matrix(new_documents)
    print(jac_mat)
    return jac_mat

jac1 = jaccard_distance(doc1, doc1)
jac2 = jaccard_distance(doc1, doc2)
jac3 = jaccard_distance(doc1, doc3)
jac4 = jaccard_distance(doc1, doc4)

mat = jaccard_matrix([doc1, doc2, doc3, doc4])

new_mat = jaccard_matrix_update(mat, [doc1, doc2, doc3, doc4], [doc5, doc6, doc3])
            
            