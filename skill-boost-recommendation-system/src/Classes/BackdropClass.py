class Backdrop:
    """
    Represents a Backdrop that contains information about an image for a particular skill

    Attributes:
        link (str): An open source image link.
        skill_type (str): The type of skill represented by the Backdrop.
    """

    def __init__(self, link, skill_type):
        """
        Initialises a new instance of the Backdrop class.

        Parameters:
            link (str): The link to the image related to the skill.
            skill_type (str): The type of skill.
        """
        self.link = link
        self.skill_type = skill_type

    def get_link(self):
        """
        Returns the link to the resource.

        Returns:
            str: The link of the resource.
        """
        return self.link

    def get_skill_type(self):
        """
        Returns the type of skill associated with the backdrop.

        Returns:
            str: The skill type.
        """
        return self.skill_type

    def to_dict(self):
        """
        Converts the Backdrop instance to a dictionary format, so it can be sent in JOSN format over the API

        Returns:
            dict: A dictionary with the link and skill type of the Backdrop.
        """
        return {
            "link": self.link,
            "skill_type": self.skill_type
        }
