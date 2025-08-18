import json
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from src.Classes.SkillClass import Skill
from src.Classes.BackdropClass import Backdrop
from src.Classes.DescriptionClass import Description
# Inserts a document into the database with the appropriate dbName.


def list_to_dict(my_list):
    new_list = []
    for item in my_list:
        new_list.append(item.to_dict())
    return new_list


def db_connect(dbName, dbFolder):
    client = MongoClient("mongodb+srv://skillset:ny-1HSames021@cluster0.rcms5tl.mongodb.net/")
    db = client[dbFolder]
    collection = db[dbName]
    return collection
def upsert_document(info,query, collection):
    # Inserts one document
    # Update the database if the link already exists, if not inserts new document
    result = collection.update_one(query, {"$set": info}, upsert=True)
    return result

def insert_document(info, collection):
    # Inserts one document
    # Update the database if the link already exists, if not inserts new document
    result = collection.insert_one(info)
    return result

# Gets the skill courses from the website ready to update.
def get_skill_courses():
    root_url = 'https://skillsbuild.org/'
    course_url = 'https://skillsbuild.org/college-students/digital-credentials'

    # Send an HTTP GET request to the URL
    response = requests.get(course_url)
    courses = []
    # Check if the request was successful (status code 200)
    if response.status_code == 200:

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        course_elements = soup.find_all('div', class_='mb-16 bx--row')
        print("Number of courses found: " + str(len(course_elements)))
        # Loop through the course elements and extract titles and links
        for course in course_elements:
            # Extract the course title
            course_title = course.find('h3', class_='bx--expressive-heading-03 mb-4')



            # Extract the course link

            course_desc = course.find('div', class_='bx--body-long-02 max-w-9/10')
         
            course_link_dir = course.find('a', class_='bx--btn bx--btn--tertiary mt-8 badge-btn mr-4')
            course_link = str(root_url + course_link_dir.get('href'))
  
            courses.append(Skill(course_title.text, "course", course_link, course_desc.text))
        return courses


    else:
        print('Failed to retrieve the webpage')

    return []

def add_backdrops(items, skill_type):
    collection = db_connect("backdrops", "skill-set-db")
    # Fetch all backdrops from the collection
    results = list(collection.find({"skill_type": skill_type}))
    # Know that there is only max len(results) photos
    if not results:
        return

    # Iterate over items and set backdrops
    for i, item in enumerate(items):
        backdrop = results[i % len(results)]
        item.set_backdrop(backdrop)


def get_skills_from_db(skill_type):
    collection = db_connect("ibm-data")
    results = list(collection.find({"skill_type": skill_type}))

    skills = []
    for result in enumerate(results):
        backdrop = Backdrop(result[1].get("backdrop").get("link"), skill_type)
        description = Description(result[1].get("description"), skill_type)
        skill = Skill(result[1].get("title"), skill_type, result[1].get("link"), backdrop, description,result[1].get("keywords"),result[1].get("likedCount"), result[1].get("recommendedCount"), result[1].get("score"))
        skills.append(skill)

    return skills

def get_skills_from_db_only(skill_type):
    collection = db_connect("skill-data", "skill-set-db")
    results = list(collection.find({"skill_type": skill_type}))
    return results

def get_one_document_from_collection(collection, var_name,var ):
    results = list(collection.find({var_name: var}))
    return results[0]

def get_tokens_from_db_only():
    collection = db_connect("tokenization-topics", "nlp-db")

    results = list(collection.find())

    return results

