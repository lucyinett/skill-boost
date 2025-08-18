class ExternalDto:
    """
    Represents an external data transfer object that holds keywords and a score.
    The score is calculated based on the number of keywords unless provided directly.
    
    Attributes:
        keywords (list): A list of keywords associated with the object.
        score (int): A score representing the object, calculated based on keyword count.
    """

    def __init__(self, keywords=None, score=None):
        """
        Initializes an ExternalDto instance either with given keywords and score or empty values.

        Parameters:
            keywords (list, optional): A list of keywords. Defaults to an empty list if not provided.
            score (int, optional): A numerical score. If not provided, it is calculated based on the number of keywords.
        """
        self.keywords = keywords if keywords is not None else []
        self.score = score if score is not None else self.calculate_score()

    def get_keywords(self):
        """
        Retrieves the keywords of the DTO.

        Returns:
            list: The keywords associated with the DTO.
        """
        return self.keywords

    def get_score(self):
        """
        Retrieves the score of the DTO.

        Returns:
            int: The score associated with the DTO.
        """
        return self.score

    def calculate_score(self):
        """
        Calculates the score based on the number of keywords.

        Returns:
            int: The score calculated as the length of the keywords list.
        """
        return len(self.keywords)

    def to_dict(self):
        """
        Converts the DTO to a dictionary format.

        Returns:
            dict: A dictionary containing keywords and score of the DTO.
        """
        return {
            "keywords": self.keywords,
            "score": self.score
        }
