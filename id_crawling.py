from bs4 import BeautifulSoup
import requests

# getting html files from clinicaltrials.gov/ct2/about-site/crawling then grap the urls to each link.
# then request to that url to scrap study ID


source = requests.get('https://clinicaltrials.gov/ct2/about-site/crawling').text

soup = BeautifulSoup(source, 'lxml')

td = soup.find('table')
for a_tag in td.find_all('a', href=True):
    print("Found URL:", a_tag['href'])
# print(td.prettify())