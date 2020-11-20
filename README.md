# AI Web Crawler 1.0

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
   `pip install -r requirements.txt`
```

3. Place the Firebase JSON into the same folder

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
