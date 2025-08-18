
class Module:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def get_title(self):
        """Returns the title of a module"""
        return self.title

    def set_title(self, new_title):
        """Updates the title of a module"""
        self.title = new_title

    def get_description(self):
        """Returns the description of a module"""
        return self.description

    def set_description(self, new_desc):
        """Updates the description of a module"""
        self.description = new_desc
