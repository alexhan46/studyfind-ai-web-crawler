from bs4 import BeautifulSoup
import requests

# getting html files from clinicaltrials.gov/ct2/about-site/crawling then grap the urls to each link.
# then request to that url to scrap study ID


source = requests.get('https://clinicaltrials.gov/ct2/about-site/crawling').text

soup = BeautifulSoup(source, 'lxml')

td = soup.find('table')
urls = td.find_all('a', href=True)
studyID_list = []
for a in urls:
    parsedURL = "https://clinicaltrials.gov" + a.get('href')
    new_source = requests.get(parsedURL).text
    new_soup = BeautifulSoup(new_source, 'lxml')
    table_for_ids = new_soup.find('table')
    ids = table_for_ids.find_all('a')
    
    for id in ids:
        studyID_list += [id.text]
        print(studyID_list)
