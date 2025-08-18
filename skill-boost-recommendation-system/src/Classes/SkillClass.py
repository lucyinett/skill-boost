from src.Classes.DescriptionClass import Description
from src.Classes.DescriptionTypeClass import DescType
from src.Classes.VectorMetric import vectorMetric
class Skill:
    """
    Represents a skill with detailed attributes, including associated metadata like type, link, and counts.

    Attributes:
        title (str): The title of the skill.
        skill_type (DescType): The type of skill, categorized by a predefined enum.
        link (str): URL link to more information about the skill.
        backdrop: Visual or contextual representation of the skill.
        description (Description): Detailed description of the skill.
        keywords (list): Keywords associated with the skill.
        likedCount (int): Number of likes this skill has received.
        recommendedCount (int): Number of times this skill has been recommended.
        score (float): An overall score representing the skill's rating or effectiveness.
    """
    def __init__(self, title, skill_type, link, backdrop, description, keywords,likedCount, recommendedCount,score):
        """
        Initializes a Skill instance with all the necessary attributes.
        """
        self.title = title
        self.skill_type = skill_type
        self.link = link
        self.backdrop = backdrop
        self.description = description
        self.keywords = keywords
        self.likedCount = likedCount
        self.recommendedCount = recommendedCount
        self.score = score


    def get_title(self):
        """Returns the title of the skill."""
        return self.title

    def set_title(self, new_title):
        """Updates the title of a skill"""
        self.title = new_title

    def get_skill_type(self):
        """Returns the type of the skill"""
        return self.skill_type

    def set_skill_type(self, new_skill_type):
        """Updates the type of the skill"""
        self.skill_type = new_skill_type

    def get_link(self):
        """Returns a link to the skills resource"""
        return self.link

    def set_link(self, new_link):
        """Updates the link for the skill"""
        self.link = new_link

    def get_backdrop(self):
        """"Returns the image background associated with the skill"""
        return self.backdrop

    def set_backdrop(self, new_backdrop):
        """Updates the image background associated with the skill"""
        self.backdrop = new_backdrop

    def get_description(self):
        """Returns the description of the skill """
        return self.description.get_description_sentence()

    def set_description(self, new_desc):
        """Updates the description of the skill """
        self.description = new_desc

    def get_keywords(self):
        """Returns the keywords of the skills obtained from the NLP system"""
        return self.description.get_keywords()

    def get_vector(self):
        """Returns the vector representation of the skill"""
        return self.description.get_vector()

    def get_score(self):
        """Returns the calculated score associated with the skill"""
        return self.score

    def get_skill_kw(self):
        """Gets the keywords stored for the skill"""
        return self.keywords

    def get_liked_count(self):
        """Returns a count of the number of times the skill has been liked"""
        return self.likedCount

    def get_recommended_count(self):
        """Returns the number of times the skill has been in the top 10 of a a recommendation"""
        return self.recommendedCount

    def to_dict(self):
        """
        Converts the skill data to a dictionary format, suitable for serialization or API responses.
        
        Returns:
            dict: Contains all the skill attributes in a dictionary form.
        """
        return{
            "title": self.title,
            "skill_type": self.skill_type,
            "link": self.link,
            "backdrop": self.backdrop.to_dict(),
            "description": self.description.get_description_sentence(),
            "keywords": self.keywords,
            "likedCount": self.likedCount,
            "recommendedCount": self.recommendedCount,
            "score": self.score

        }


