from typing import List, Dict
from datetime import datetime as date, time
import urllib.request
from bs4 import BeautifulSoup
import requests
# adding fake User-Agent because our program is running in background
from fake_useragent import UserAgent 
import os.path
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
    if data is None:
        return None
    while(len(data) != 0):
        id, study = data.popitem(last=False)
        out[study["ID"]] = study["last_updated"]
    return out


# Given a dict mapping study ids to last updated time, gets a list of study ids that we haven't seen before

def get_study_ids(last_study_id) -> Dict[str, date]:
    ua = UserAgent()
    header = {'user-agent':ua.chrome}
    newly_added_studyIDs_list = {}

    # getting html files from clinicaltrials.gov/ct2/about-site/crawling then grap the urls linking each subpages.
    source = requests.get('https://clinicaltrials.gov/ct2/about-site/crawling', headers=header, timeout= 30).text
    soup = BeautifulSoup(source, 'lxml')

    table = soup.find('table')

    urls_to_each_pages = table.find_all('a', href=True)

    for a_tag in urls_to_each_pages:
        # Get range of studyID as list
        range = (a_tag.next_sibling.split(" to "))
        # Convert ['NCTxxxxxxx', 'NCTxxxxxxx'] to [xxxxxx, xxxxxx]
        range = list(map(lambda x: int(x[3:]), range))

        # search studies thta is created after given last_study_id
        if(last_study_id<=range[0] or last_study_id<=range[1]):
            
            parsedURL = "https://clinicaltrials.gov" + a_tag.get('href')
            new_source = requests.get(parsedURL, headers=header, timeout= 30).text
            source_html_per_page = BeautifulSoup(new_source, 'lxml')
            table_for_ids = source_html_per_page.find('table')
            ids = table_for_ids.find_all('a')
            
            for id in ids:
                id.string.replace_with(id.text[3:])
                if (int(id.text) > last_study_id):
                    newly_added_studyIDs_list[id.text] = None
    return newly_added_studyIDs_list


# Given a study id, downloads and formats the data, and returns a Study object
def download_and_format(id: str) -> Study:
    id = "NCT" + id
    print(id)
    url = "https://clinicaltrials.gov/ct2/show/" + id + "?resultsxml=true"
    try: 
        rawdata = urllib.request.urlopen(url)
    except urllib.error.HTTPError as exception:
        print(exception)
        return None

    data = BeautifulSoup(rawdata.read(), "lxml-xml")

    #foramtting 
    title = data.find("official_title").get_text()
    description = data.find("brief_summary").get_text()
            
    date_str = data.find("last_update_posted").get_text()
    last_updated = date.strptime(date_str, '%B %d, %Y')
            
    study_type = data.find("study_type").get_text() if data.find("study_type") != None else None

    conditions = []
    for condition in data.findAll("condition"):
        conditions.append(condition.get_text())
    
    #lead sponsor only (no collborators)
    sponsor = data.find("lead_sponsor").find("agency").get_text() 
    recruitment_status = data.find("overall_status").get_text() 
            
    age = {"min":data.find("minimum_age").get_text(), "max":data.find("maximum_age").get_text()}
            
    sex = data.find("gender").get_text() if data.find("gender") != None else None
    control = data.find("healthy_volunteers").get_text() if data.find("healthy_volunteers") != None else None
    additional_criteria = data.find("criteria").get_text() if data.find("criteria") != None else None

    locations = []
    for loc in data.findAll("location"):
        name = loc.find("name").get_text() if loc.find("name") != None else None
        country = loc.find("country").get_text() if loc.find("country") != None else None
        city = loc.find("city").get_text() if loc.find("city") != None else None
        zipcode = loc.find("zip").get_text() if loc.find("zip") != None else None
        status = loc.find("status").get_text() if loc.find("status") != None else None
        locations.append({"name": name, "country": country, "city": city, "zipcode": zipcode, "status": status})

    contact = data.find("overall_contact")
    if contact is not None:
        contactName = contact.find("last_name").get_text() if contact.find("last_name") != None else None
        contactPhone = contact.find("phone").get_text() if contact.find("phone") != None else None
        contactEmail = contact.find("email").get_text() if contact.find("email") != None else None
    else:
        contactName, contactPhone, contactEmail = None, None, None

    return Study(title, description, last_updated, id, study_type, condition, sponsor, recruitment_status,
                age, sex, control, additional_criteria, locations, contactName, contactPhone, contactEmail)



# Executes the crawler, by getting new studies, download their data, and exporting it to the database

def crawl():

    # TODO below code will work when the import and export database function
    existing_studies = import_study_ids_from_database()

    # existing_studies = {}
    
    # TODO sample last study id is 4557501. This must be replaced by dynamically changed based on what value has in database
    new_studies = get_study_ids(4557501)

    existing_studies.update(new_studies)


    # TODO have to take care of handling errors. For now, when there is no fields, the code exits with error. 
    # For example, NCT04557891 doesn't have description or other information. 
    studies = [download_and_format(study_id) for study_id in existing_studies]

    export_studies_to_database(studies)


# TODO: Schedule crawler to run based on parameters from admin panel
def main():
    crawl()

if __name__ == "__main__":
    main()