from typing import List, Dict
from datetime import datetime as date, time
import urllib.request
from bs4 import BeautifulSoup

# Defines the parameters from the admin panel


class Parameters:

    def __init__(self, dot: str, t: time):
        self.day_of_the_week = dot
        self.time = t

# Defines a study object
class Study:
    def __init__(self, title: str, description: str, last_updated: date, ID: str, study_type: str,
                 conditions: List[str], sponsor: str, recruitment_status: str, age: (int, int, str), 
                 sex: str, control: str, additional_criteria: str, locations: List[Dict[str, str]],
                 contactName: str, contactPhone: str, contactEmail: str):
        self.title = title
        self.description = description
        self.last_updated = last_updated
        self.ID = ID
        self.type = study_type
        self.conditions = conditions
        self.sponsor = sponsor
        self.recruitment_status = recruitment_status
        self.age = age
        self.sex = sex
        self.control = control
        self.additional_criteria = additional_criteria
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
    url = "https://clinicaltrials.gov/ct2/show/" + id + "?resultsxml=true"
    rawdata = urllib.request.urlopen(url)

    # Request not successfully processed
    if rawdata.getcode() != 200:  
        return None

    data = BeautifulSoup(rawdata.read(), "lxml-xml")

    #foramtting 
    title = data.find("official_title").get_text()
    description = data.find("brief_summary").get_text()
            
    date_str = data.find("last_update_posted").get_text()
    last_updated = date.strptime(date_str, '%B %d, %Y')
            
    study_type = data.find("study_type").get_text()

    conditions = []
    for condition in data.findAll("condition"):
        conditions.append(condition)
        
    sponsor = data.find("lead_sponsor").find("agency").get_text() ##lead sponsor only (no collborators)
    recruitment_status = data.find("overall_status").get_text()
            
    age = {"min":data.find("minimum_age").get_text(), "max":data.find("maximum_age").get_text()}
            
    sex = data.find("gender").get_text()
    control = data.find("healthy_volunteers").get_text()
    additional_criteria = data.find("criteria").get_text()

    locations = []
    if data.findAll("location") is not None:
        for loc in data.findAll("location"):
            localLocation = loc.find("name").get_text()
            nationalLocation = loc.find("address").get_text().strip("\n").replace("\n", ", ")
            locations.append({"locationLocation": localLocation, "nationalLocation": nationalLocation, "status": status})

    contact = data.find("overall_contact")
    if contact is not None:
        contactName = contact.find("last_name").get_text()
        contactPhone = contact.find("phone").get_text()
        contactEmail = contact.find("email").get_text()

    return Study(title, description, last_updated, id, study_type, condition, sponsor, recruitment_status,
                age, sex, control, additional_criteria, locations, contactName, contactPhone, contactEmail)

# Executes the crawler, by getting new studies, download their data, and exporting it to the database

def crawl():

    new_studies = get_study_ids(import_study_ids_from_database())

    studies = [download_and_format(study_id) for study_id in new_studies]

    export_studies_to_database(studies)


# TODO: Schedule crawler to run based on parameters from admin panel
