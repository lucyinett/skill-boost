import re
from src.NlpSys.nlp_functions import clean_data, tokenize, stem
from src.Classes.keywordClass import Keyword
from enum import Enum


class PhraseType(str, Enum):
    """
    Enumeration for distinguishing between types of phrases.

    This enum is used to categorize phrases based on their complexity or structure,
    which can influence how they are processed or displayed in the application.

    Attributes:
        MULTI (str): Represents phrases that are composed of multiple elements or sub-phrases.
        NORMAL (str): Represents standard, single-component phrases.
    """
    MUTLI = "Multi"
    NORMAL = "Normal"


class Nlp:
    """
    Represents the NLP service and the different values needed to process the sentence to create a keyword profile.

    """
    def __init__(self, sentence):
        self.sentence = sentence
        self.keywords: [Keyword] = []
        self.search_type = None

    # Constructors

    def get_sentence(self):
        return self.sentence

    def add_keyword(self, phrase):
        keyword = Keyword(phrase, "cs", PhraseType.NORMAL)
        self.keywords.append(keyword)

    def set_keywords(self, keywords):
        self.keywords = keywords

    def set_search_type(self, search_type):
        self.search_type = search_type

    def get_keywords(self):
        return self.keywords

    def get_keyword_phrases(self):
        phrases = []
        for word in self.keywords:
            phrases.append(word.get_phrase())
        return phrases

    def apply_nlp_functions(self):
        """Apply NLP functions to initial sentence."""
        self.clean_data()
        self.tokenize()

    def clean_data(self):
        """Clean the initial sentence."""
        self.keywords = clean_data(self.sentence)

    def tokenize(self):
        """Tokenize the cleaned data."""
        self.keywords = tokenize(self.keywords)

    def stem(self):
        """Remove punctuation marks from tokens."""
