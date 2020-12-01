# AI Web Crawler 1.0
[![Automated Release Notes by gren](https://img.shields.io/badge/%F0%9F%A4%96-release%20notes-00B2EE.svg)](https://github.com/alexhan46/studyfind-ai-web-crawler/)
[![All Contributors](https://img.shields.io/badge/all_contributors-5-orange.svg?style=flat-square)](#contributors-)

AI Web Crawler is a python tool that downloads data about available research studies, formats it, and uploads the data to a database.

Coded in Python v3.8.5

## Relesae Notes

> ## v1.0.0 (20/11/2020)
>
> #### New Features
>
> - [#7](https://github.com/alexhan46/studyfind-ai-web-crawle/issues/7)
>   [#8](https://github.com/alexhan46/studyfind-ai-web-crawle/issues/8)  [#9](https://github.com/alexhan46/studyfind-ai-web-crawle/issues/9)  [#15](https://github.com/alexhan46/studyfind-ai-web-crawle/issues/15)  [#25](https://github.com/alexhan46/studyfind-ai-web-crawle/issues/25)
>   Download research studies by crawling clinicaltrials.gov=
> - [#6](https://github.com/alexhan46/studyfind-ai-web-crawle/issues/6)  [#26](https://github.com/alexhan46/studyfind-ai-web-crawle/issues/26)
>   Schedule crawling tasks to run on a recurring basis
> - [#27](https://github.com/alexhan46/studyfind-ai-web-crawle/issues/27)
>   [#33](https://github.com/alexhan46/studyfind-ai-web-crawle/issues/33)
>   Use NLP to create a brief summary and a list of keywords for each crawler
> - Automatically upload the data to the specified Firebase database
> - [#34](https://github.com/alexhan46/studyfind-ai-web-crawle/issues/34)
>   Use multithreading for superior performance (up to 7 studies per sec)
>
> #### Bug Fixes
>
> - The crawler didn't run if there was http request errors(fixed)

## Installation Guide

### Requirements

- Python 3 (recommended [3.8.5](https://www.python.org/downloads/release/python-385/))
- Pip (included with Python 3)
- The Firebase JSON provided by the development team

### Installation

1. Download the code using `git` or straight from GitHub
2. To install dependencies, execute the following command where the code was downloaded

```
   pip install -r requirements.txt
```
3. Run the following commands to install other required dependencies

```
  python -m nltk.downloader stopwords
  python -m nltk.downloader universal_tagset
  python -m spacy download en
```

4. Place the Firebase JSON into the same folder

### Usage

There are 2 ways to execute the crawler

A. Using the admin panel to schedule recurring crawls

```
python manage.py runserver
```

To use the admin panel, you must be an authorized user, with access to the login information

b. Manually executing the crawler

```
python crawler.py
```

## Known Limitations

- When updating studies that have already been crawled, there is a limitation placed by clinicaltrials.gov, causing some studies to be left out. In our testing we have never gotten close to this limit as long as the crawler is executed daily.


## Contributors ✨

Meet our team mates

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/adeeb897"><img src="https://avatars1.githubusercontent.com/u/13613663?s=460&v=4" width="100px;" alt=""/><br /><sub><b>Adeeb Zaman</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/joheeju"><img src="https://avatars1.githubusercontent.com/u/31485229?s=460&u=3a9ec697656d5171102d81d4fcd1e4dd89a666cd&v=4" width="100px;" alt=""/><br /><sub><b>Heejoo Cho</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/jsisson7"><img src="https://avatars1.githubusercontent.com/u/70162294?s=460&v=4" width="100px;" alt=""/><br /><sub><b>Jonathon Sisson</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/jkim3389"><img src="https://avatars0.githubusercontent.com/u/45981964?s=460&v=4" width="100px;" alt=""/><br /><sub><b>Juntae Kim</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/alexhan46"><img src="https://avatars2.githubusercontent.com/u/3508584?s=460&u=1b618325e26851b4509532038b6b24845d66edd9&v=4" width="100px;" alt=""/><br /><sub><b>Alex Han</b></sub></a><br /></td>
  </tr>
</table>
