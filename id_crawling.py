from bs4 import BeautifulSoup
import requests

# getting html files from clinicaltrials.gov/ct2/about-site/crawling then grap the urls to each link.
# then request to that url to scrap study ID


source = requests.get('https://clinicaltrials.gov/ct2/about-site/crawling').text
source_html_all = BeautifulSoup(source, 'lxml')

td = source_html_all.find('table')
urls_to_each_pages = td.find_all('a', href=True)
studyID_list = []
for a_tag in urls_to_each_pages:
    parsedURL = "https://clinicaltrials.gov" + a_tag.get('href')
    new_source = requests.get(parsedURL).text
    source_html_per_page = BeautifulSoup(new_source, 'lxml')
    table_for_ids = source_html_per_page.find('table')
    ids = table_for_ids.find_all('a')
    
    for id in ids:
        studyID_list += [id.text]
        print(id.text)