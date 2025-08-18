from enum import Enum

class PhraseType(str, Enum):
    """
    Enumeration for distinguishing between types of phrases.

    This enum is used to categorize phrases based on their complexity or structure,
    which can influence how they are processed or displayed in the application.

    Attributes:
        MULTI (str): Represents phrases that are composed of multiple elements or sub-phrases.
        NORMAL (str): Represents standard, single-component phrases.
    """
    MULTI = "Multi"  # Multi-component phrases, possibly requiring special handling.
    NORMAL = "Normal"  # Standard, straightforward phrases.

class Keyword:
    """
    Represents a keyword or phrase within the application, with associated metadata.

    This class encapsulates a phrase, its type, and the topic it relates to, providing
    methods to access these properties and to perform basic operations like checking
    the existence of the phrase in a list.

    Attributes:
        phrase (str): The actual phrase or keyword.
        topic: The topic or category to which the phrase is related.
        type (PhraseType): The type of the phrase, as defined by the PhraseType enum.
    """

    def __init__(self, phrase: str, phrase_topic, phrase_type: PhraseType):
        """
        Initializes a new instance of Keyword.

        Parameters:
            phrase (str): The text of the phrase or keyword.
            phrase_topic: The topic or category associated with the phrase.
            phrase_type (PhraseType): The enumerated type of the phrase.
        """
        self.phrase = phrase
        self.topic = phrase_topic
        self.type = phrase_type

    def get_phrase(self):
        """
        Retrieves the phrase.

        Returns:
            str: The phrase of this Keyword object.
        """
        return self.phrase

    def get_type(self):
        """
        Retrieves the type of the phrase.

        Returns:
            PhraseType: The type of the phrase as an enumerated value.
        """
        return self.type

    def get_topic(self):
        """
        Retrieves the topic associated with the phrase.

        Returns:
            The topic of the phrase. Type depends on how topics are represented in the application.
        """
        return self.topic

    def to_dictionary(self):
        """
        Converts the Keyword object to a dictionary format.

        Returns:
            dict: A dictionary containing the phrase and its type.
        """
        return {'phrase': self.phrase, 'type': self.type}

    def exists_in(self, new_list):
        """
        Checks whether the phrase exists in a provided list of Keyword objects.

        Parameters:
            new_list (list): A list of Keyword objects to check against.

        Returns:
            bool: True if the phrase exists in the list, False otherwise.
        """
        for item in new_list:
            if item.get_phrase() == self.phrase:
                return True
        return False
