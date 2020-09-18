from typing import List, Dict
from datetime import datetime as date, time
import urllib.request

# Defines the parameters from the admin panel


class Parameters:

    def __init__(self, dotw: str, t: time):
        self.day_of_the_week = dotw
        self.time = t

# Defines a study object
#
# INPUT FORMAT
# title:
# description:
# last_updated:
# ID:
# study_type:
# conditions:
# sponsor:
# recruitment_status: "Recruiting" or "Completed" or ..
# age: (min, max, unit)
# sex: "All" or "Female" or "Male"
# control:
# additional_criteria:
# locations: list of {"name": , "country": , "city": , "zipcode": , "status": }
# contact: {"name": , "phone": , "email": }

class Study:
    def __init__(self, title: str, description: str, last_updated: date, ID: str, study_type: str,
                 conditions: List[str], sponsor: str, recruitment_status: str, age: (int, int, str), 
                 sex: str, control: str, additional_criteria: str, locations: List[Dict[str, str]],
                 contact: Dict[str, str]):
        self.title = title
        self.description = description
        self.last_updated = last_updated
        self.ID = ID
        self.type = study_type
        self.conditions = conditions
        self.sponsor = sponsor
        self.recruitment_status = recruitmentStatus
        self.age = age
        self.sex = sex
        self.control = control
        self.additional_criteria = additionalCriteria
        self.locations = locations
        self.contact = contact

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
    description = "" #TODO #summary?
        
    date_str = data.find("last_update_posted").get_text()
    last_updated = date.strptime(date_str, '%B %d, %Y')
        
    study_type = data.find("study_type").get_text()
    condition = [] #TODO 
    sponsor = data.find("lead_sponsor").find("agency").get_text() ##lead sponsor and collborators
    recruitment_status = data.find("overall_status").get_text()
        
    min_age = data.find("minimum_age").get_text()
    max_age = data.find("maximum_age").get_text()
    unit = min_age[min_age.index(" ")+1:]
    age = (int("".join(filter(str.isdigit, min_age))), 
            int("".join(filter(str.isdigit, max_age))), unit)
        
    sex = data.find("gender").get_text()
    control = "" #TODO #??
    additional_criteria = "" #TODO #inclusion/exclusion

    locations = []
    for loc in data.findAll("location"):
        name = loc.find("name").get_text()
        country = loc.find("country").get_text()
        city = loc.find("city").get_text()
        zipcode = loc.find("zip").get_text()
        status = loc.find("status").get_text()
        locations.append({"name": name, "country": country, "city": city, "zipcode": zipcode, "status": status})

    contact = {}
    c = data.find("overall_contact")
    if c is not None:
        contact["name"] = c.find("last_name").get_text()
        contact["phone"] = c.find("phone").get_text()
        contact["email"] = c.find("email").get_text()

    return Study(title, description, last_updated, id, study_type, condition, sponsor, recruitment_status,
                age, sex, control, additional_criteria, locations, contact)

# Executes the crawler, by getting new studies, download their data, and exporting it to the database
def crawl():

    new_studies = get_study_ids(import_study_ids_from_database())

    studies = [download_and_format(study_id) for study_id in new_studies]

    export_studies_to_database(studies)


# TODO: Schedule crawler to run based on parameters from admin panel
