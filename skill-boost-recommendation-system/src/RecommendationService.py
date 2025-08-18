import time
import gensim
import gensim.downloader as api
from src.Classes.VectorMetric import VectorMetric
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


def bow(keywords):
    dictionary = {}
    for kw in keywords:
        title = f"<pseudo-document:{kw}>"
        body = ": ".join(list(set(kw.split())))
        dictionary[title] = body

    # Initialize CountVectorizer
    vectorizer = CountVectorizer(min_df=0.0, ngram_range=(1.0,1.0))

    # Construct BoW matrix
    bow_matrix = vectorizer.fit_transform(dictionary.values()).astype(float)

    # Display first few rows of the BoW matrix
    print("Sample Bow Matrix:\n", bow_matrix.toarray())
    #print("Sample Bow Matrix:\n", bow_matrix.toarray()[0:5].round(2))
    return bow_matrix.toarray()

def keyword_to_vector(keyword, model):
    tokens = keyword.split()
    word_vectors = []
    for token in tokens:
        if token in model:
            word_vectors.append(model[token])

    if len(word_vectors) > 0:
        return np.mean(word_vectors, axis=0)
    else:
        return np.zeros(model.vector_size)  # return zero vector if no valid word vectors found




def wrd_embedding(kws, vec_model):
    vec = []
    if kws is None:
        print("No keywords to vectorize")
        return 0
    for word in kws:
        vect = (keyword_to_vector(word, vec_model))
        vec.append(vect)

    kws_set_avg = np.mean(vec, axis=0)  # Average pooling for set 1

    set_embedding = kws_set_avg.reshape(1, -1)

    return set_embedding

def cluster_embedding(kws, vec_model):
    vec = []
    if kws is None:
        print("No keywords to vectorize")
        return 0
    for word in kws:
        vect = (keyword_to_vector(word, vec_model))
        vec.append(vect)


    return vec


def extractVector(keywords, metric, model):

    if metric == VectorMetric.BOW:
        return bow(keywords)
    elif metric == VectorMetric.WRDEMBEDDING:
        return wrd_embedding(keywords, model)












