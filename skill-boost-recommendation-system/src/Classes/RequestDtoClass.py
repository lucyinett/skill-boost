from pydantic import BaseModel
from typing import List

class RequestDto(BaseModel):
    """
    Represents a general request data transfer object (DTO) for user requests.

    Attributes:
        type (str): Specifies the type of the request, helping in routing or processing the request.
        description (str): Provides a detailed description or additional context about the request.
    """
    type: str
    description: str

class GraphRequest(BaseModel):
    """
    Represents a request for operations related to graph-based data structures or algorithms.

    Attributes:
        k (int): identifies the number of clusters for k-means clustering
    """
    k: int

class ClusterRequest(BaseModel):
    """
    Represents a request specifically for clustering operations, typically in data analysis or machine learning contexts.

    Attributes:
        keywordProfile (str): A string identifier or keyword that profiles or categorizes the clustering request,
                              which could be used to apply specific clustering logic or parameters.
    """
    keywordProfile: str
