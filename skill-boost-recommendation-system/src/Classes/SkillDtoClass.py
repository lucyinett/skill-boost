from SkillClass import Skill

class SkillDto:
    """
    Repreents a skill that has not yet been processed by the NLP system

    Attributes:
        skill_date (Skill): information about the skill
        keywords (Array[String]) Set of words produced by the NLP based off of the skill data

     """
    def __init__(self, skill_data, keywords):
        """
        Initializes a SkillDto instance with all the necessary attributes.
        """
        self.skill_data = skill_data
        self.keywords = keywords

    def __init__(self, skill):
        self.skill_data = skill
        self.keywords = []
    def get_skill_data(self):
        """Returns the skill data for the skill"""
        return self.skill_data

    def get_skill_data_title(self):
        """Returns the title associated with the skill data"""
        return self.skill_data.get_title()

    def get_skill_data_link(self):
        """Returns the link associated with the skill data"""
        return self.skill_data.get_link()

    def get_skill_data_description(self):
        """Returns the description associated with the skill data"""
        return self.skill_data.get_description()

    def get_skill_data_skill_type(self):
        """Returns the skill type associated with the skill data"""
        return self.skill_data.get_skill_type()

    def get_skill_data_backdrop(self):
        """Returns the backdrop associated with the skill data"""
        return self.skill_data.get_backdrop()

    def get_keywords(self):
        """Returns the keywords associated with the skill data"""
        return self.keywords

    def to_dict(self):
        """
        Converts the skill data to a dictionary format, suitable for serialisation or API responses.
        
        Returns:
            dict: Contains all the skill attributes in a dictionary form.
        """
        return{
            "skill_data": self.skill_data.to_dict(),
            "keywords": self.keywords
        }
