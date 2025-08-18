from src.Classes.nlpClass import Nlp
from src.NlpSys.nlp_functions import filter_keywords


def nlp_for_data(description):
    """
    Calculates the keywords associated with a description from data.
    
    Returns:
        List of keywords.
    """
    to_process = Nlp(description)

    to_process.apply_nlp_functions()
    return to_process.get_keyword_phrases()


def nlp_for_user(description):
    """
    Calculates the keywords associated with a description from a user.
    
    Returns:
        List of keywords.
    """
    to_process = Nlp(description)

    to_process.apply_nlp_functions()

    return to_process.get_keyword_phrases()

