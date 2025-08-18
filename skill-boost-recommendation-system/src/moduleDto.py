##
class ModuleDto:
    def __init__(self, keywords):
        self.keywords = keywords

    def __init__(self, module):
        self.keywords = [] 
    def get_keywords(self):
        """Returns the keywords of a module"""
        return self.keywords

    def to_dict(self):
        """Converts the ModuleDto into a dictionary"""
        return {
            "keywords": self.keywords
        }




