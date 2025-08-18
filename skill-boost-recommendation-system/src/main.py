import pickle

from fastapi import FastAPI, Depends
from gensim.models import Word2Vec

from src.Classes.RequestTypeClass import RequestType
from src.databaseActions import get_skills_from_db, list_to_dict, get_cs_words
from src.RecommendationController import processRecommendtion
from src.Classes.DescriptionClass import Description
from src.Classes.DescriptionTypeClass import DescType
from src.Classes.RequestDtoClass import RequestDto, GraphRequest, ClusterRequest
from src.Classes.VectorMetric import vectorMetric
from src.Classes.SimilarityScoreType import SimilarityScoreType
from src.Classes.RequestClass import Request
from src.Classes.VectorModel import MLModel, get_model
from src.scripts import plot_k_means, create_dummy_recommendations, classify_new_item, recommend_similar_users
app = FastAPI()

"""Load the serialised vecotrisation model"""
'''with open('word2vec.pkl', 'rb') as f:
    model_instance = pickle.load(f)'''

model_instance = MLModel().model


@app.on_event("startup")
async def startup_event():
    pass

"""
       Processes a user request and returns a recomemndation

        Returns:
            List[Skill]: Recommended skills based on the input.
        """
@app.post("/recommendation")
async def get_recom(data: RequestDto, model = Depends(lambda: model_instance)):
    if len(data.description) != 0:
        desc = Description(data.description, DescType.User, vectorMetric(), model)
        if len(desc.get_keywords()) == 0:
            return []
        request = Request(desc, RequestType(data.type))
        similarityMetric = SimilarityScoreType.Cosine
        response = processRecommendtion(request, vectorMetric(), similarityMetric, model)
        response_list = (list_to_dict(response))
        return response_list[:min(12, len(response_list))]
        # return processRecommendtion(Request(desc, RequestType(data.type)), vectorMetric())
    else:
        return []
    
"""
        Assigns a cluster based off of a user profile

        Returns:
            int: Cluster number assigned to the user keyword profile.
        """
@app.post("/get-cluster")
async def get_graph(data: ClusterRequest, model = Depends(lambda: model_instance)):

    kwArr = data.keywordProfile.split(", ")
    print(kwArr)
    similar_users = recommend_similar_users(model, kwArr)
    return similar_users
