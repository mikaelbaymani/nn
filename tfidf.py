import numpy as np


def norm(x):
    sum_sq = x.dot( x.T )
    norm = np.sqrt( sum_sq )
    return ( norm )


def compute_tf( wordDict, bagOfWords ):
    tfDict = {}
    bagOfWordsCount = len( bagOfWords )
    for word, count in wordDict.items():
        tfDict[word] = count / float( bagOfWordsCount )
    return tfDict


def compute_idf( documents ):
    import math
    N = len( documents )

    idfDict = dict.fromkeys( documents[0].keys(), 0 )
    for document in documents:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1

    for word, val in idfDict.items():
        idfDict[word] = math.log( N / float(val) )
    return idfDict


def compute_tfidf( tfBagOfWords, idfs ):
    tfidf = {}
    for word, val in tfBagOfWords.items():
        tfidf[word] = val * idfs[word]
    return tfidf


def cosine_distance( x, y ):
    xy = x.dot( y.T )
    dist = xy / ( norm(x)*norm(y) )
    return 1-dist[0, 0]
