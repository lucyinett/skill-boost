import datetime
import pickle
import random
import time
from faker import Faker
from bson import ObjectId
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from fastapi import FastAPI
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import pandas as pd
from src.Classes.DescriptionTypeClass import DescType
from src.Classes.VectorMetric import vectorMetric
from src.databaseActions import get_tokens_from_db_only, list_to_dict, get_skills_from_db_only, upsert_document, db_connect, insert_document, get_one_document_from_collection
from src.Classes.VectorMetric import vectorMetric
from src.NlpSys.nlp_controller import nlp_for_data
from sklearn.metrics.pairwise import cosine_similarity
from src.RecommendationService import extractVector, cluster_embedding
from src.Classes.SkillClass import Skill
from src.Classes.BackdropClass import Backdrop
from src.Classes.SkillClass import Description
import gensim
import gensim.downloader as api
import json

import bson
import numpy as np

"""
These are the functions used for the data pre-processing. They are not used currently by the sysem.
But they were used to generate data used by the system, such as assigning a keyword profile to each
skill in the database and generating the k-means clustering graph.

"""

def set_skill():
    """Generate keywords for each of the items in the database"""
    collection = db_connect("warwick-catalogue", "skill-set-db")
    for result in enumerate(collection.find()):
        # Perform upsert
        words_to_extract = result[1].get("description").replace("\n", " ") + " " + result[1].get("title")

        kws = nlp_for_data(words_to_extract)

        query = {"courseCode":  result[1].get("courseCode")}
        new_kw = {"keywords": kws}
        new_code = {"shortCourseCode": result[1].get("courseCode").split("-")[0]}
        result = upsert_document(new_kw, query, collection)
        result = upsert_document(new_code, query, collection)


def list_to_json(data, split_on_str):
    data_list = []
    for item in data:
        output_list = [item.strip() for item in item.lower().split(split_on_str) if item]
        data_dict = {"abbreviation": output_list[0], "phrase": output_list[1]}
        data_list.append(data_dict)

    return json.dumps(data_list)


def unset_attribute(attribute: str, collectionName):
    tokens = db_connect(collectionName, "nlp-db")

    tokens.update_many({}, {"$unset": {attribute: ""}})


def get_user_keyword_profile(userId):
    # get a list of recommendations from the user
    collection = db_connect("users", "skill-set-db")
    recommendations = get_one_document_from_collection(collection,"_id", ObjectId(userId)).get("userHistory")

    all_skills = []
    # for each recommendation, get the list of skills been recommended
    for recommendation in recommendations:
        collection = db_connect("recommendation", "skill-set-db")
        skills = get_one_document_from_collection(collection, "_id", recommendation).get("recommendedCourses")

        all_skills += skills

    keywords = []
    # for each skill, get the keywords
    for skill in all_skills:
        collection = db_connect("skill-data", "skill-set-db")
        kws = get_one_document_from_collection(collection, "_id", skill).get("keywords")
        print(kws)
        keywords += kws

    distinct_kws = set(keywords)
    return list(distinct_kws)

def plot_k_means(model, k):
    # Get the Word2Vec vectors for each course description

    # for each user want to concat all of the keywords from their recommended courses and plot them
    collection = db_connect("users", "skill-set-db")
    skills = list(collection.find())
    skill_vectors = []
    skill_user = []
    user_no_history = []
    for skill in skills:
        kw = skill.get("keyword_profile")
        if kw:
            kw_vect = extractVector(kw,vectorMetric(),model)
            skill_vectors.append(kw_vect)
            skill_user.append([skill.get("_id")])
        else:
            user_no_history.append([skill.get("_id")])



    # Sample word embeddings (replace with your actual embeddings)
    word_embeddings = np.array(skill_vectors)

    # Flatten the embeddings to make them 2D
    flattened_embeddings = word_embeddings.reshape(word_embeddings.shape[0], -1)

    # Reduce dimensionality to 2D using PCA
    pca = PCA(n_components=2)
    embeddings_2d = pca.fit_transform(flattened_embeddings)



    # Initialize KMeans model
    kmeans = KMeans(n_clusters=k, random_state=42)

    # Fit the model to the 2D embeddings
    kmeans.fit(embeddings_2d)

    # Get cluster assignments for each embedding
    cluster_assignments = kmeans.labels_


    i = 0
 
    for cluster_num in cluster_assignments:

        skill_user[i].append(int(cluster_assignments[i]))
        i += 1

    for user in user_no_history:
        user.append(-1)

    '''Update the users' group'''
    update_users = user_no_history + skill_user
    for item in update_users:
        query = {"_id": item[0]}
        info = {"userGroup": item[1]}
        upsert_document(info, query, collection)




 
    plt.figure(figsize=(8, 6))
    for i in range(k):
        plt.scatter(embeddings_2d[cluster_assignments == i, 0], embeddings_2d[cluster_assignments == i, 1],
                    label=f'Cluster {i + 1}')

    plt.title('User Keyword Profile Clusters')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend()
    plt.show()

    # Save the fitted model to a file
    with open('kmeans_model_users.pkl', 'wb') as f:
        pickle.dump(kmeans, f)

    # Save the pca model to a file
    with open('pca_model_users.pkl', 'wb') as f:
        pickle.dump(pca, f)


def recommend_similar_users(model, kws):

    cluster = classify_new_item(model, kws)
    return cluster





def classify_new_item(model, kws):
    with open('kmeans_model_users.pkl', 'rb') as f:
        kmeans = pickle.load(f)

    with open('pca_model_users.pkl', 'rb') as f:
        pca = pickle.load(f)
    vect = extractVector(kws, vectorMetric(), model)

    # Flatten the word embedding
    flattened_embedding = vect.flatten()

    # Reshape the flattened embedding into a 2D array with a single row
    flattened_embedding_2d = flattened_embedding.reshape(1, -1)

    embedding_2d = pca.transform(flattened_embedding_2d)

    # Predict the cluster for the preprocessed word embedding
    cluster_label = kmeans.predict(embedding_2d)

    print("Predicted Cluster:", cluster_label[0]+1)
    return int(cluster_label[0])



def load_software():

    path_dir = '../data/software.txt'
    backdrops_dir = '../data/backdrops.json'
    raw_software = open(path_dir, "r")
    items = []
    titles = []
    backdrop_json = open(backdrops_dir, "r")
    all_backdrops = json.load(backdrop_json)

    '''Load the first 8 items which are the backdrops for the software'''
    software_backdrops = []
    for i in range(0,8):
        software_backdrops.append(all_backdrops[i])


    count = 0
    for i in range(0,50):

        title = raw_software.readline().replace("Title: ","").replace("\n", "")
        desc = raw_software.readline().replace("Description: ","").replace("\n", "")
        link = raw_software.readline().split("(")[1].replace(")","").replace("\n", "").replace("\r", "")
        raw_software.readline()

        item = {"title": title, "skill_type": "software", "link": link,"backdrop": software_backdrops[count],"description": desc, "keywords": []}
        items.append(item)
        title = {"topicPhrase": title.lower(), "topicType": "cs"}
        titles.append(title)


        if count == 7:
            count = 0
        else:
            count += 1

    file = open("../data/software.json", 'w')
    json.dump(items, file, indent=4)

    return titles

def load_events():

    path_dir = '../data/events.txt'
    backdrops_dir = '../data/backdrops.json'
    raw_event = open(path_dir, "r")
    items = []
    titles = []
    backdrop_json = open(backdrops_dir, "r")
    all_backdrops = json.load(backdrop_json)

    '''Load the first 8 items which are the backdrops for the software'''
    event_backdrops = []
    for i in range(8,17):
        event_backdrops.append(all_backdrops[i])

    link = "https://www.eventbrite.co.uk"

    count = 0
    for i in range(0,50):

        title = raw_event.readline().replace("Title: ", "").replace("\n", "")
        desc = raw_event.readline().replace("Description: ", "").replace("\n", "")
        details = raw_event.readline().replace("Details: ", "").replace("\n", "")
        description = details + ". "+ desc
        raw_event.readline()


        item = {"title": title, "skill_type": "event", "link": link,"backdrop": event_backdrops[count], "description": description, "keywords": []}
        items.append(item)
        title = {"topicPhrase": title.lower(), "topicType": "cs"}
        titles.append(title)


        if count == 7:
            count = 0
        else:
            count += 1

    file = open("../data/event.json", 'w')
    json.dump(items, file, indent=4)


    file = open("../data/new_words.json", 'w')
    json.dump(titles, file, indent=4)



def create_dummy_recommendations(model):
    fake = Faker()

    # Generate example users
    users = []
    for _ in range(20):
        name = fake.name()

        # Specify start and end dates
        start_date = datetime.datetime(2020, 1, 1)  # Example start date (year, month, day)
        end_date = datetime.datetime.now()  # Example end date (current date)

        # Generate a fake timestamp between the start and end dates
        timestamp = str(fake.date_time_between(start_date, end_date))
        username = name.lower().replace(" ", "")
        email = username + "@email.com"
        password = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
        userHistory = []

        info = {"username":username, "email":email, "name":name, "password":password , "userHistory":userHistory}

        collection = db_connect("users", "skill-set-db")
        new_user = insert_document(info, collection)
        new_userId = ObjectId(new_user.inserted_id)

        # generate a random number of skills for the user, between 3 and 10
        skills = get_skills_from_db_only("course")
        skill_ids = [skill.get("_id") for skill in skills]
        # generate a random number of times the user has used the system, between 1 and 5 recommendations done by each user
        for _ in range(0, random.randint(1, 5)):

            user_skill_selection = random.sample(skill_ids, k=random.randint(3, 10))


            recommendation_info = {"userId":new_userId, "timestamp": timestamp, "recommendedCourses": user_skill_selection}

            # Insert the new recommendations into the system
            collection = db_connect("recommendation", "skill-set-db")
            new_recommendation = insert_document(recommendation_info, collection)

            # Get the new recommendation id
            new_recommendationId = ObjectId(new_recommendation.inserted_id)

            # Add the recommendation id to the user's history
            collection = db_connect("users", "skill-set-db")
            user_to_update = {"_id":new_userId}

            # Update the document to add the new element to the array
            update_result = collection.update_one(user_to_update, {'$push': {'userHistory': new_recommendationId}})

def add_user_kw_profile():

    # Get a list of userIds
    collection = db_connect("users", "skill-set-db")
    users = collection.find()
    userIds =  [user.get("_id") for user in users]


    for userId in userIds:
        user_to_update = {"_id": ObjectId(userId)}
        kw_profile = get_user_keyword_profile(userId)
        if kw_profile is not None:
            collection.update_one(user_to_update, {"$set": {'keyword_profile': kw_profile}}, upsert=True)

def add_skill_initial_scores():
    collection = db_connect("skill-data", "skill-set-db")
    recommendatons = collection.find()
    recomIds = [recom.get("_id") for recom in recommendatons]

    for recomId in recomIds:
        recom_to_update = {"_id": ObjectId(recomId)}

        collection.update_one(recom_to_update, {"$set": {'recommendedCount': 0}}, upsert=True)
        collection.update_one(recom_to_update, {"$set": {'likedCount': 0}}, upsert=True)
        collection.update_one(recom_to_update, {"$set": {'score': 0}}, upsert=True)




def clean_recommendations():
    collection = db_connect("recommendation", "skill-set-db")
    user_collection = db_connect("users", "skill-set-db")
    recommendatons = collection.find({"likedSkills":{"$exists": False}})
    inactive = set()
    for recom in recommendatons:
        recom.get("userId")
        inactive.add(recom.get("userId"))
        if not user_collection.find({"_id": recom.get("userId")}):
            inactive.add(recom.get("userId"))


