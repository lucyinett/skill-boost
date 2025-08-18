import numpy as np
import gensim

from src.Classes.DescriptionClass import Description
from  src.Classes.RequestSkillScoreClass import RequestSkillScore
from  src.Classes.RequestTypeClass import RequestType
from src.Classes.SkillClass import Skill
from src.UtilityFunctions import normalize_vector_linalg
from src.Classes.SimilarityScoreType import SimilarityScoreType
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA


class Request:
    """ 
    Represents a user search request, encapsulating all information entered by the user for their search.
    Attributes:
        description (Description): The actual input from the user describing their search.
        request_type (RequestType): The type of search the user has made.
        scores (list of RequestSkillScore): A sorted list of skill scores related to the request.
        alpha (float): Weight factor used in scoring feedback mechanisms.
        hasScore (bool): Flag indicating if the request has any scores.
    """
    def __init__(self, description: Description, request_type: RequestType):
        """
        Initialises a new Request instance.
        
        Parameters:
            description (Description): Description of the search request.
            request_type (RequestType): Type of the request.
        """
        self.description : Description = description
        self.request_type : RequestType = request_type
        self.scores: [RequestSkillScore] = []
        self.alpha = 0.1
        if self.scores is None:
            self.hasScore: bool = False
        else:
            self.hasScore: bool = True

    
    def set_scores(self, newScores: [RequestSkillScore]):
        self.scores = sorted(newScores, key=lambda x: x.score, reverse=True)
        """
    Sets and sorts the scores for the request based on the score value.
    
    Parameters:
        newScores (list of RequestSkillScore): New scores to be added.
    """
    
    def add_score(self, newScore: RequestSkillScore):
        """
            Adds a new score to the scores list and sorts it.
            
            Parameters:
                newScore (RequestSkillScore): The new score to add.
        """   

        self.scores.append(newScore)

        self.scores = sorted(self.scores, key=lambda x: x.score, reverse=True)


    def normalize(self, skill_vector):
        """
        Normalizes and pads the skill and request vectors to the same length.
        
        Parameters:
            skill_vector (np.array): Vector to normalize.
        
        Returns:
            tuple: Normalized and padded skill and request vectors.
        """
        skill_vector = np.ravel(skill_vector)
        request_vector = np.ravel(self.get_vector())
        skill_vector_norm = normalize_vector_linalg(skill_vector)
        request_vector_norm = normalize_vector_linalg(request_vector)
        max_dim = max(skill_vector_norm.shape[0], request_vector_norm.shape[0])
        if skill_vector_norm.shape[0] < max_dim:
            skill_vector_norm = np.pad(skill_vector_norm, (0, max_dim - skill_vector_norm.shape[0]), mode='constant')
        if request_vector_norm.shape[0] < max_dim:
            request_vector_norm = np.pad(request_vector_norm, (0, max_dim - request_vector_norm.shape[0]), mode='constant')
        return skill_vector_norm, request_vector_norm
    
    
    def score_skill(self, skills: [Skill], metric):
        """
        Scores each skill in a list using the specified metric and updates the scores list.
        
        Parameters:
            skills (list of Skill): List of skills to score.
            metric (SimilarityScoreType): The metric to use for scoring.
        
        Returns:
            list of RequestSkillScore: Updated list of scores.
        """
        for skill in skills:
            metric_request_score = 0
            if metric == SimilarityScoreType.Cosine:
                metric_request_score = self.add_wrd_embed_score(skill)

            self.add_feedback_score(metric_request_score)

        return self.scores

    def add_feedback_score(self, metric_score):
        """
        Adjusts a metric score by incorporating feedback, then adds the updated score to the list.
        
        Parameters:
            metric_score (RequestSkillScore): The metric score to adjust.
        """
        skill_feedback_score = self.alpha * float(metric_score.get_skill().get_score())
        altered_score = float(skill_feedback_score) + float(metric_score.get_score())
        metric_score.set_score(altered_score)
        self.add_score(metric_score)

    def get_request_type(self) -> RequestType:
        """
        Returns the type of the request.
        
        Returns:
            RequestType: The request type.
        """
        return self.request_type

    def get_vector(self):
        """
        Retrieves the vector representation of the description.
        
        Returns:
            np.array: Vector representation of the description.
        """
        return self.description.get_vector()

    def get_score(self):
        """
        Returns the current list of scores.
        
        Returns:
            list of RequestSkillScore: The current scores.
        """
        return self.scores

    def cosine_metric(self, norm_skill, norm_request):
        """
        Calculates the cosine similarity between two normalized vectors.
        
        Parameters:
            norm_skill (np.array): Normalized skill vector.
            norm_request (np.array): Normalized request vector.
        
        Returns:
            float: The cosine similarity score.
        """
        cos_sim = np.dot(norm_skill, norm_request)
        return cos_sim

    def add_bow_score(self, skill):
        """
        Calculates and adds a score based on Bag-of-Words (BoW) model for the given skill.
        
        Parameters:
            skill (Skill): The skill to score.
        """
        norm_skill, norm_request = self.normalize(skill.get_vector())

        cosine_score = self.cosine_metric(norm_skill, norm_request)

        # Function to convert a keyword to a vector representation

        new_score = RequestSkillScore(cosine_score, skill)
        self.add_score(new_score)


    def add_wrd_embed_score(self, skill):
        """
        Calculates and adds a word embedding score for the given skill based on cosine similarity.
        
        Parameters:
            skill (Skill): The skill to score.
        
        Returns:
            RequestSkillScore: The new score based on the similarity of the skills and the description
        """
        similarity_matrix = cosine_similarity(skill.get_vector(), self.get_vector())

        average_similarity = np.mean(similarity_matrix)
        new_score = RequestSkillScore(average_similarity, skill)
        return new_score
