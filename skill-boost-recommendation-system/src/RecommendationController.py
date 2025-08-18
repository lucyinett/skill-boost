from src.Classes.BackdropClass import Backdrop
from src.Classes.DescriptionClass import Description
from src.Classes.RequestClass import Request
from src.Classes.RequestTypeClass import RequestType
from src.Classes.SimilarityScoreType import SimilarityScoreType
from src.Classes.DescriptionTypeClass import DescType
from src.Classes.SkillClass import Skill

from src.databaseActions import get_skills_from_db_only


def processRecommendtion(request: Request, vector_metric, similarityMetric, model):
    # Get the keywords from the description
    response = []
    """Get all of the relevant skills from the database"""
    skills = get_skills(request, vector_metric, model)
    """Score each of the skills compared to the search request"""
    recom = request.score_skill(skills, similarityMetric)
    """Create an ordered list of skills"""
    for skill in recom:
        response.append(skill.get_skill())

    return response


def get_skills(request, metric, model):
    """Gets all of the skills from the database based on the users search filter"""
    if request.get_request_type() == RequestType.All:
        course_skill = get_skills_from_db_only(RequestType.Course)
        software_skill = get_skills_from_db_only(RequestType.Software)
        event_skill = get_skills_from_db_only(RequestType.Event)
        db_skills = course_skill + software_skill + event_skill
    elif request.get_request_type() == RequestType.CourseSoftware:
        course_skill = get_skills_from_db_only(RequestType.Course)
        software_skill = get_skills_from_db_only(RequestType.Software)
        db_skills = course_skill + software_skill
    elif request.get_request_type() == RequestType.CourseEvent:
        course_skill = get_skills_from_db_only(RequestType.Course)
        event_skill = get_skills_from_db_only(RequestType.Event)
        db_skills = course_skill + event_skill
    elif request.get_request_type() == RequestType.SoftwareEvent:
        software_skill = get_skills_from_db_only(RequestType.Software)
        event_skill = get_skills_from_db_only(RequestType.Event)
        db_skills = software_skill + event_skill
    else:
        db_skills = get_skills_from_db_only(request.get_request_type())
    skills = []
    for result in enumerate(db_skills):
        backdrop = Backdrop(result[1].get("backdrop").get("link"), request.get_request_type())
        description = Description(result[1].get("description"),DescType.Data, metric, model, result[1].get("keywords"))
        skill = Skill(result[1].get("title"),result[1].get("skill_type"), result[1].get("link"), backdrop, description,result[1].get("keywords"),result[1].get("likedCount"), result[1].get("recommendedCount"), float(result[1].get("score")))

        skills.append(skill)
    return skills