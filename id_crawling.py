from  bs4 import BeautifulSoup
import requests
# adding fake User-Agent because our program is running in background
from fake_useragent import UserAgent 
import os.path


# study_id_base_index refer to the starting studyid to be crawled
def study_id_crawling(last_study_id):
    
    last_study_id = int(last_study_id[3:])
    ua = UserAgent()
    header = {'user-agent':ua.chrome}
    newly_added_studyIDs_list = []

    # getting html files from clinicaltrials.gov/ct2/about-site/crawling then grap the urls linking each subpages.
    try:
        response = requests.get('https://clinicaltrials.gov/ct2/about-site/crawling', headers=header, timeout= 30)
        source = response.text
    except Exception:
        print("failed to fetch url. Re-attemped to fetch again")
        return study_id_crawling(last_study_id)
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
            new_source_response = requests.get(parsedURL, headers=header, timeout= 30)
            new_source = new_source_response.text
            source_html_per_page = BeautifulSoup(new_source, 'lxml')
            table_for_ids = source_html_per_page.find('table')
            ids = table_for_ids.find_all('a')
            
            for id in ids:
                if (int(id.text[3:]) > last_study_id):
                    newly_added_studyIDs_list.append(id.text)

    # print(newly_added_studyIDs_list)
    # (Test Purpose) exit early when they get 10000 study ids due to large volume 
    #     if(len(new_studyID_list) > 10000):
    #         break
    return newly_added_studyIDs_list


# Testing purpose to generate result file to output folder
def writeFileForTestPurpose(filename, list):
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    if(not os.path.exists(fileDir+"/output")):
        os.mkdir(fileDir+"/output")
    relPath = 'output/'+filename+'.txt'
    path = os.path.join(fileDir, relPath)
    with open(path, 'w') as f:
        for item in list:
            f.write("%s\n" % item)

# Test script with sample number of study id
def main():
    study_id_crawling("NCT04557501")

if __name__ == "__main__":
    main()