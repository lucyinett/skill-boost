from pymongo import MongoClient
import re



def db_connect(dbName):
    """Connect to the external database"""
    client = MongoClient("mongodb+srv://skillset:ny-1HSames021@cluster0.rcms5tl.mongodb.net/")
    db = client["nlp-db"]
    collection = db[dbName]
    return collection


def get_multi_tokens_from_db(token_list):
    # Connect to the NLP database
    collection = db_connect("tokenization-topics")

    # Query the database to see if any of the tokens are in the database
    query = {"topicPhrase": {"$regex": r'\b({})\b'.format('|'.join(map(re.escape, token_list))), "$options": "i"}}
    projection = {"_id": 0, "topicPhrase": 1, "topicType": 1, "aka": 1}
    cursor = list(collection.find(query, projection))
    print("cursor is...")
    print(cursor)
    return cursor
    # get the phrases that match

def get_abbreviations_from_db(token_list):
    # Connect to the NLP database
    collection = db_connect("tokenization-topics")

    # Query the database to see if any of the tokens are in the database
    query = {"abbreviation": {"$regex": r'\b({})\b'.format('|'.join(map(re.escape, token_list))), "$options": "i"}}
    projection = {"_id": 0, "abbreviation": 1, "topicPhrase": 1}
    cursor = collection.find(query, projection)
    return list(cursor)
    # get the phrases that match
