from typing import List, Dict
from datetime import datetime as date, time
import urllib.request
from bs4 import BeautifulSoup
import pyrebase
import feedparser
import time
from id_crawling import study_id_crawling
from gensim.summarization import keywords
from gensim.summarization.summarizer import summarize
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
import threading
import time


DB_TABLE = "test"

config = {
  "apiKey": "AIzaSyC4wlsU_QkOjD1MhT2Im-IAXZAkd5uuFiE",
  "authDomain": "crawlerdata-4fb83.firebaseapp.com",
  "databaseURL": "https://crawlerdata-4fb83.firebaseio.com",
  "storageBucket": "crawlerdata-4fb83.appspot.com",
  "serviceAccount": "crawlerdata-4fb83-firebase-adminsdk-qdzwv-1264b2c7f5.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

crawled = 0

# Defines a study object
class Study:
    def __init__(self, title: str, summary: str, description: str, last_updated: date, ID: str, study_type: str,
                 conditions: List[str], sponsor: str, recruitment_status: str, age: (int, int, str), 
                 sex: str, control: str, additional_criteria: str, locations: List[Dict[str, str]],
                 contactName: str, contactPhone: str, contactEmail: str, keywordLists: List[str]):
        self.title = title
        self.summary = summary
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
        self.NLP_summary = None
        #Adding keyword section
        self.keywordLists = keywordLists

    # String representation of a Study
    def set_NLP_summary(self, summary: str):
        self.NLP_summary = summary

    def __str__(self):
        return f'{self.title} (ID: {self.ID}): {self.summary}'


# Given a Study object, exports the data to our database
def export_study_to_database(studyvar: Study):
    idnum = studyvar.ID
    db.child(DB_TABLE).child(idnum).child("title").set(studyvar.title)
    db.child(DB_TABLE).child(idnum).child("summary").set(studyvar.summary)
    db.child(DB_TABLE).child(idnum).child("description").set(studyvar.description)
    db.child(DB_TABLE).child(idnum).child("last_updated").set(str(studyvar.last_updated))
    db.child(DB_TABLE).child(idnum).child("ID").set(studyvar.ID)
    db.child(DB_TABLE).child(idnum).child("type").set(studyvar.type)
    db.child(DB_TABLE).child(idnum).child("conditions").set(studyvar.conditions)
    db.child(DB_TABLE).child(idnum).child("sponsor").set(studyvar.sponsor)
    db.child(DB_TABLE).child(idnum).child("recruitmentStatus").set(studyvar.recruitment_status)
    db.child(DB_TABLE).child(idnum).child("age").set(studyvar.age)
    db.child(DB_TABLE).child(idnum).child("sex").set(studyvar.sex)
    db.child(DB_TABLE).child(idnum).child("control").set(studyvar.control)
    db.child(DB_TABLE).child(idnum).child("additionalCriteria").set(studyvar.additional_criteria)
    db.child(DB_TABLE).child(idnum).child("locations").set(studyvar.locations)
    db.child(DB_TABLE).child(idnum).child("contactName").set(studyvar.contactName)
    db.child(DB_TABLE).child(idnum).child("contactPhone").set(studyvar.contactPhone)
    db.child(DB_TABLE).child(idnum).child("contactEmail").set(studyvar.contactEmail)
    db.child(DB_TABLE).child(idnum).child("NLPSummary").set(studyvar.NLP_summary)

    #add keyword section
    db.child(DB_TABLE).child(idnum).child("keywordLists").set(studyvar.keywordLists)


# Downloads studies from our database, and returns as a list of Study objects
def import_studies_from_database() -> List[Study]:
    data = db.child(DB_TABLE).get()
    data = data.val()
    out = []
    if data is None:
        return None
    while(len(data) != 0):
        id, study = data.popitem(last=False)
        newstudy = Study(study["title"], study["summary"], study["description"], study["last_updated"], study["ID"], study["type"], study["conditions"], study["sponsor"], study["recruitmentStatus"], study["age"], study["sex"], study["control"], study["additionalCriteria"], study["locations"], study["contactName"], study["contactPhone"], study["contactEmail"], study['keywordLists'])
        newstudy.set_NLP_summary(study["NLPSummary"])
        out.append(newstudy)

    return out


# Downloads study ids and the last updated timestamp for that study from our database and returns as a Dict
def import_study_ids_from_database() -> Dict[str, date]:
    data = db.child(DB_TABLE).get()
    data = data.val()
    out = {}
    if data is None:
        return None
    while(len(data) != 0):
        id, study = data.popitem(last=False)
        out[study["ID"]] = study["last_updated"]
    return out

def export_last_updated(date: str):
    db.child("last_updated").set(date)

def import_last_updated() -> str:
    data = db.child("last_updated").get().val()
    return "0/0/0000" if data is None else data

def export_latest_study_id(study_id: str):
    db.child("latest_study").set(study_id)

def import_latest_study_id() -> str:
    data = db.child("latest_study").get().val()
    return "NCT11111111" if data is None else data


# Given the date of the last updated study, return a list of studies that have been updated since then
def get_study_ids(last_updated) -> List[str]:
    d = feedparser.parse("https://clinicaltrials.gov/ct2/results/rss.xml?rcv_d=&lup_d=14&sel_rss=mod14&lupd_s=" + last_updated + "&lupd_e=" + time.strftime("%m/%d/%Y") + "&count=100000")['entries']
    
    if len(d) < 1000: # Max number of studies
        return [x['id'] for x in d]
    else:
        # Find studies that were left out by combining filters to avoid limits
        d = []
        rTypes = ['a', 'b', 'e', 'f', 'd', 'g', 'h', 'i', 'm']
        sTypes = ['Intr', 'Obsr', 'PReg', 'Expn']
        for r in rTypes:
            for s in sTypes:
                url = "https://clinicaltrials.gov/ct2/results/rss.xml?rcv_d=&lup_d=14&sel_rss=mod14&lupd_s=" + last_updated + "&lupd_e=" + time.strftime("%m/%d/%Y") + "&count=100000&type=" + s + "&recrs=" + r
                d += feedparser.parse(url)['entries']
        return [x['id'] for x in d]

def get_new_study_ids(latest_study) -> List[str]:
    return study_id_crawling(latest_study)


# Given a study id, downloads and formats the data, and returns a Study object
def download_and_format(id: str) -> Study:
    url = "https://clinicaltrials.gov/ct2/show/" + id + "?resultsxml=true"
    try: 
        rawdata = urllib.request.urlopen(url)
    except urllib.error.HTTPError as exception:
        return None

    data = BeautifulSoup(rawdata.read(), "lxml-xml")

    #foramtting 
    title = data.find("official_title").get_text() if data.find("official_title") else None
    description = " ".join(data.find("detailed_description").get_text().split()) if data.find("detailed_description") != None else None
    summary = " ".join(data.find("brief_summary").get_text().split()) if data.find("brief_summary") != None else None

    NLP_summary = None
    if description is not None:
        NLP_summary = NLP_summarize(description)
    elif summary is not None:
        NLP_summary = NLP_summarize(summary)

    ################ Adding keywords by NLP
    if description is not None:
        keywordLists = keywords(description, words=5).split('\n')
    else:
         keywordLists = None

    # print("studyID is..",id,"the keywords are..", keywordLists)
    
    ################

    date_str = data.find("last_update_posted").get_text() if data.find("last_update_posted") != None else None
    last_updated = date.strptime(date_str, '%B %d, %Y')
            
    study_type = data.find("study_type").get_text() if data.find("study_type") != None else None

    conditions = []
    for condition in data.findAll("condition"):
        if condition != None:
            conditions.append(condition.get_text())
    
    #lead sponsor only (no collborators)
    sponsor = data.find("lead_sponsor").find("agency").get_text() if data.find("lead_sponsor") and data.find("lead_sponsor").find("agency") else None
    recruitment_status = data.find("overall_status").get_text() if data.find("overall_status") else None
            
    age = {"min":data.find("minimum_age").get_text() if data.find("minimum_age") else None, "max":data.find("maximum_age").get_text() if data.find("maximum_age") else None}
            
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

    study = Study(title, summary, description, last_updated, id, study_type, conditions, sponsor, recruitment_status,
                age, sex, control, additional_criteria, locations, contactName, contactPhone, contactEmail, keywordLists)

    study.set_NLP_summary(NLP_summary)

    return study


def NLP_summarize(description: str):

    # Object of automatic summarization.
    auto_abstractor = AutoAbstractor()
    # Set tokenizer.
    auto_abstractor.tokenizable_doc = SimpleTokenizer()
    # Set delimiter for making a list of sentence.
    auto_abstractor.delimiter_list = [".", "\n"]
    # Object of abstracting and filtering document.
    abstractable_doc = TopNRankAbstractor()
    # Summarize document.
    result_dict = auto_abstractor.summarize(description, abstractable_doc)

    # Output result.
    maxi = [0, 0]
    for result in result_dict["scoring_data"]:
        if maxi[1] < result[1]:
            maxi = result

    if maxi[0] < len(result_dict["summarize_result"]):
        return result_dict["summarize_result"][maxi[0]]
    else:
        return None


# Downloads a list of study ids and export it to the database
def download_and_export(study_ids: List[str], run_event) -> str:

    global crawled

    for i, study_id in enumerate(study_ids):

        if run_event.is_set():
            while True:
                try:

                    # Download the study
                    study = download_and_format(study_id)

                    # Upload the study to our database
                    export_study_to_database(study)

                    break

                except Exception as e:
                    # Pause to prevent overloading the server
                    time.sleep(10)


            crawled += 1

        else:
            break


# Executes the crawler, by getting new studies, download their data, and exporting it to the database
def crawl():

    print("\nChecking which studies need to be updated...")

    study_ids = get_new_study_ids(import_latest_study_id()) + get_study_ids(import_last_updated())

    study_ids = list(dict.fromkeys(study_ids)) # removes duplicates

    print("\nFound " + str(len(study_ids)) + " studies\n")

    print("\nRetrieving studies....\n")

    printProgressBar(0, len(study_ids), prefix = 'Progress:', suffix = 'Complete', length = 50)

    startTime = time.time()

    N = 4 # Number of chunks/threads to split studies into

    run_event = threading.Event() # Allows us to interrupt threads
    run_event.set()

    # Separate chunks of study_ids into N threads
    threads = [threading.Thread(target=download_and_export, args=(chunk_of_studies, run_event)) for chunk_of_studies in chunks(study_ids, N)]

    global crawled

    [t.start() for t in threads]

    try:
        while crawled < len(study_ids):
            printProgressBar(crawled, len(study_ids), prefix = 'Progress:', suffix = 'Complete', length = 50, printEnd = " - Speed: " + str(round((crawled)/(time.time() - startTime), 2)) + " studies/sec \r")
    except KeyboardInterrupt:
        print("\n\nCanceling...")
        run_event.clear()

    # Wait for threads to finish
    [t.join() for t in threads]

    if run_event.is_set():
        # Update last_updated date with the max id
        export_last_updated(time.strftime("%m/%d/%Y")) 
        if len(study_ids) > 0:

            maxId = None
            for i in study_ids:
                if maxId is None or int(maxId[3:]) < int(i[3:]):
                    maxId = i

            export_latest_study_id(maxId)

    print('\nFinished!\n')


# Yield successive n-sized chunks from lst 
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


# TODO: Schedule crawler to run based on parameters from admin panel
def main():
    crawl()

if __name__ == "__main__":  
    main()

