import time

import gensim
import gensim.downloader as api

class MLModel:
    """
    A class to encapsulate the machine learning model, specifically a Word2Vec model.
    This class handles the instantiation and provides a method to access the model.
    """
    def __init__(self):
        """
        Initializes the MLModel instance by loading a pre-trained Word2Vec model that has been pickled.
        """
        self.model = load_word2vec_model()

def get_model():
    """
    Retrieves the loaded Word2Vec model.
    
    Returns:
        gensim.models.KeyedVectors: The loaded Word2Vec model.
    """
    return MLModel().model


def load_word2vec_model():
    """
    Loads a pre-trained Word2Vec model from gensim's model repository.

    This function utilizes Gensim's API to download and load the 'word2vec-google-news-300' model,
    which is a pre-trained model on Google News dataset (about 100 billion words).
    The model consists of 300-dimensional vectors for 3 million words and phrases.

    Returns:
        gensim.models.KeyedVectors: The loaded Word2Vec model, ready to use.
    """
    path = api.load("word2vec-google-news-300", return_path=True)
    word2vec_model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
    return word2vec_model
