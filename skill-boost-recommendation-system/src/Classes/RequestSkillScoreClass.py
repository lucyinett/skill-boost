

class RequestSkillScore:
    """ 
    Represents the score of each of the inputs for the skill request:
       score (float): the calculated score for the similarity between a skill and a given decription
    """
    def __init__(self,score, skill):
        """
        Initialises a new RequestSkillScore instance.
        """
        self.score = score
        self.skill = skill

    def get_score(self):
        """
        Returns the score for the skill.
        
        Returns:
            Float: The score.
        """ 
        return self.score

    def set_score(self, score):
        """
        Sets the new score for the skill similarity.
        
        """
        self.score = score

    def get_skill(self):
        """
        Returns the skill.
        
        Returns:
            Skill: The skill being compared.
        """
        return self.skill

    def to_dict(self):
        """
        Converts the Skill into a dictionary item to be sent as a JSON oject
        
        Returns:
            Skill Dictionary: Converted skill object.
        """
        return {
            "title": self.skill.get_.title(),
            "skill_type": self.skill.get_skill_type(),
            "link": self.skill.get_.link(),
            "backdrop": self.skill.get_backdrop().to_dict(),
            "description": self.skill.get_.description()
        }

    def a_to_dict(self):
        return {'score': self.score, 'skill title': self.skill.get_title(), "skill kws": self.skill.get_keywords()}
    
