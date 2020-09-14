from typing import List, Dict
from datetime import datetime as date, time


# Defines the parameters from the admin panel
class Parameters:

    def __init__(self, dotw: str, t: time):
        self.day_of_the_week = dotw
        self.time = t


# Defines a study object
class Study:
    def __init__(self, title: str, description: str, last_updated: date, ID: str, sType: str,
            conditions: List[str], sponsor: str, recruitmentStatus: str, age: str, sex: str,
            control: str, additionalCriteria: str, locations: List[Dict[str, str]], contactName: str, contactPhone: str, contactEmail: str):
        self.title = title
        self.description = description
        self.last_updated = last_updated
        self.ID = ID
        self.type = sType
        self.conditions = conditions
        self.sponsor = sponsor
        self.recruitmentStatus = recruitmentStatus
        self.age = age
        self.sex = sex
        self.control = control
        self.additionalCriteria = additionalCriteria
        self.locations = locations
        self.contactName = contactName
        self.contactPhone = contactPhone
        self.contactEmail = contactEmail


    # String representation of a Study
    def __str__(self):
        return f'{self.title} (ID: {self.ID}): {self.description}'


# Given a list of Study objects, exports the data to our database
def export_studies_to_database(studies: List[Study]):

    pass


# Downloads studies from our database, and returns as a list of Study objects
def import_studies_from_database() -> List[Study]:
    
    return None


# Downloads study ids and the last updated timestamp for that study from our database and returns as a Dict
def import_study_ids_from_database() -> Dict[str, date]:
    
    return None


# Given a dict mapping study ids to last updated time, gets a list of study ids that we haven't seen before
def get_study_ids(studies: Dict[str, date]) -> List[str]:
    
    return None


# Given a study id, downloads and formats the data, and returns a Study object
def download_and_format(id: str) -> Study:

    return None


# Executes the crawler, by getting new studies, download their data, and exporting it to the database
def crawl():

    new_studies = get_study_ids(import_study_ids_from_database())

    studies = [download_and_format(study_id) for study_id in new_studies]

    export_studies_to_database(studies)


# TODO: Schedule crawler to run based on parameters from admin panel