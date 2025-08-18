import re
import nltk
from pymongo import MongoClient

nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from nltk.stem.snowball import SnowballStemmer
st = SnowballStemmer('english')


from src.NlpSys.nlp_repository import get_multi_tokens_from_db, get_abbreviations_from_db
from src.Classes.keywordClass import Keyword
from enum import Enum



class PhraseType(str, Enum):
    MUTLI = "Multi"
    NORMAL = "Normal"
    AKA = "Aka"
    MODULE = "Module"

def remove_punctuation(txt):
    # Define the regex pattern to match punctuation
    pattern = r'[!"#$%&\'()*,./:;<=>?@[\]^_`{|}~]'  # Add any additional punctuation characters as needed

    # Use the re.sub() function to replace matches with an empty string
    text_without_punctuation = re.sub(pattern, '', txt)

    return text_without_punctuation

def clean_data(txt):

    # Change to lowercase and remove extra spaces either side
    cleaned_txt = txt.lower().strip()
    # Remove extra spaces inbetween the text
    cleaned_txt = re.sub(' +', ' ', cleaned_txt)

    # remove selected punctuation
    cleaned_txt = remove_punctuation(cleaned_txt)

    return cleaned_txt

def get_multi_tokens(txt_tokens: list):
    # Get matching multi-tokens from the database
    matching_multi_tokens = get_multi_tokens_from_db(txt_tokens)

    # Filter the words to remove repeated matches
    filtered_tokens = []
    for document in matching_multi_tokens:

        phrase = document.get("topicPhrase")

        if phrase in " ".join(txt_tokens):
            filtered_tokens.append(Keyword(phrase, document["topicType"], PhraseType.MUTLI))
        aka = document.get("aka")

        if aka is not None:
            txt_tokens_string = " ".join(txt_tokens)  # Convert txt_tokens to a single string
            for alt_word in aka:
                if alt_word in txt_tokens_string:
                    filtered_tokens.append(Keyword(phrase, document["topicType"], PhraseType.AKA))

    # Filter to remove partial matches
    filtered_txt = filter_keywords(filtered_tokens)
    return filtered_txt

# abbreviations are only ever one word but will be considered to be a multi-token. Needs to be done before multitokens
def replace_abbreviations(tokens: list):

    abbr_list = get_abbreviations_from_db(tokens)

    for abbr in abbr_list:

        tokens[tokens.index(abbr["abbreviation"])] = abbr["topicPhrase"]
    return tokens

def replace_module(sentence):
    sentence = sentence.lower()
    client = MongoClient("mongodb+srv://skillset:ny-1HSames021@cluster0.rcms5tl.mongodb.net/")
    db = client["skill-set-db"]
    collection = db["warwick-catalogue"]
    answer = []
    # Check if the sentence contains the short or long course code
    for result in enumerate(collection.find()):

        if result[1].get("courseCode").lower() in sentence or result[1].get("shortCourseCode").lower() in sentence or result[1].get("title").lower() in sentence:
  
            for kw in enumerate(result[1]["keywords"]):

                answer.append(Keyword(kw[1], "cs", PhraseType.MODULE))

    return answer
    # Check if the sentence contains the title of a module

def tokenize(cleaned_txt):
    # check for course codes

    module_kw = list(set(replace_module(cleaned_txt)))
    # Tokenize topic phrases
    split_words = nltk.word_tokenize(cleaned_txt)

    # Remove any abbreviations in the text - all lower case
    full_split_words = replace_abbreviations(split_words)

    # Get matching multi-tokens from the database
    matching_multi_tokens = get_multi_tokens(full_split_words)


    all_kws = matching_multi_tokens + module_kw

    return list(set(all_kws))


def filter_keywords(keywords):
    filtered = []
    keywords.sort(key=lambda x: len(x.get_phrase()), reverse=True)

    for i, keyword in enumerate(keywords):
        phrase = keyword.get_phrase()

        if keyword.get_type() != PhraseType.MUTLI:
            filtered.append(keyword)
        elif not any(set(phrase).issubset(other.phrase) and phrase != other.phrase for other in keywords[:i]) and not keyword.exists_in(filtered):
            filtered.append(keyword)

    return filtered


def stem(keywords):

    # remove stopwords and get the stem of each word
    cleaned_txt = ' '.join(st.stem(text) for text in keywords if text not in stop_words)

    return cleaned_txt


