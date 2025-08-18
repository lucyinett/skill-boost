from enum import Enum
"""
Identifies which method is being used to calculate similarity between vectors
    
"""
class SimilarityScoreType(str, Enum):
    Cosine = "cosine",
    Jaccard = "jaccard"