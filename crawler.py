from typing import List, Dict
from datetime import datetime as date, time
import pyrebase

config = {
  "apiKey": "AIzaSyC4wlsU_QkOjD1MhT2Im-IAXZAkd5uuFiE",
  "authDomain": "crawlerdata-4fb83.firebaseapp.com",
  "databaseURL": "https://crawlerdata-4fb83.firebaseio.com",
  "storageBucket": "crawlerdata-4fb83.appspot.com",
  "serviceAccount": "crawlerdata-4fb83-firebase-adminsdk-qdzwv-1264b2c7f5.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

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
    for studyvar in studies:
        idnum = studyvar.ID
        db.child("test").child(idnum).child("title").set(studyvar.title)
        db.child("test").child(idnum).child("description").set(studyvar.description)
        db.child("test").child(idnum).child("last_updated").set(studyvar.last_updated)
        db.child("test").child(idnum).child("ID").set(studyvar.ID)
        db.child("test").child(idnum).child("type").set(studyvar.type)
        db.child("test").child(idnum).child("conditions").set(studyvar.conditions)
        db.child("test").child(idnum).child("sponsor").set(studyvar.sponsor)
        db.child("test").child(idnum).child("recruitmentStatus").set(studyvar.recruitmentStatus)
        db.child("test").child(idnum).child("age").set(studyvar.age)
        db.child("test").child(idnum).child("sex").set(studyvar.sex)
        db.child("test").child(idnum).child("control").set(studyvar.control)
        db.child("test").child(idnum).child("additionalCriteria").set(studyvar.additionalCriteria)
        db.child("test").child(idnum).child("locations").set(studyvar.locations)
        db.child("test").child(idnum).child("contactName").set(studyvar.contactName)
        db.child("test").child(idnum).child("contactPhone").set(studyvar.contactPhone)
        db.child("test").child(idnum).child("contactEmail").set(studyvar.contactEmail)
        

    pass


# Downloads studies from our database, and returns as a list of Study objects
def import_studies_from_database() -> List[Study]:
    data = db.child("test").get()
    data = data.val()
    out = []
    if data is None:
        return None
    while(len(data) != 0):
        id, study = data.popitem(last=False)
        newstudy = Study(study["title"], study["description"], study["last_updated"], study["ID"], study["type"], study["conditions"], study["sponsor"], study["recruitmentStatus"], study["age"], study["sex"], study["control"], study["additionalCriteria"], study["locations"], study["contactName"], study["contactPhone"], study["contactEmail"])
        out.append(newstudy)

    return out


# Downloads study ids and the last updated timestamp for that study from our database and returns as a Dict
def import_study_ids_from_database() -> Dict[str, date]:
    data = db.child("test").get()
    data = data.val()
    out = {}
    while(len(data) != 0):
        id, study = data.popitem(last=False)
        out[study["ID"]] = study["last_updated"]
    return out


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


#Test the Database Functions
"""testingstudy = Study("THE SEQUEL", "GOODBYE DataBase", "When I get BACKK", "123", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1")
testinglist = [testingstudy]
export_studies_to_database(testinglist)
outlist = import_studies_from_database()
print(outlist[0])
print(import_study_ids_from_database())"""
import_study_ids_from_database()