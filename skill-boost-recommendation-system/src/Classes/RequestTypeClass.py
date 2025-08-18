from enum import Enum
"""
   Represents the different search filters that a user can have on their search
    
"""
class RequestType(str, Enum):
    Course = "course",
    Software = "software",
    Event = "event",
    All = "all",
    CourseSoftware = "cs",
    CourseEvent = "ce",
    SoftwareEvent = "se"
