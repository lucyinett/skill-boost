
class RecommendaitonHistory:

    def __init__(self, prompt, recommendation, feedback):
        self.prompt = prompt
        self.recommendation = recommendation
        self.feedback = feedback

    def get_prompt(self):
        """returns the prompt associated with a recommendation"""
        return self.prompt

    def get_recommendation(self):
        """Return a recommendation in the user history"""
        return self.recommendation

    def get_feedback(self):
        """Returns the feedback score associated with the recommendation"""
        return self.feedback
    