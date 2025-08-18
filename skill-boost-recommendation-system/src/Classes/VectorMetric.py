from enum import Enum
"""

    Identifies the method being used to convert the keywords into a vector
"""
class VectorMetric(str, Enum):
    BOW = "bow",
    WRDEMBEDDING = "word embedding"

'''Set the vector metric being used here '''

def vectorMetric():
    return VectorMetric.WRDEMBEDDING

