
import requests

import random

from bs4 import BeautifulSoup as bs

def scrapeWikiArticle(url):
    response = requests.get(
        url = url,
    )

    soup = bs(response.content, 'html.parser')

    title = soup.find(id = 'firstHeading')

    print(title.text)

    allLinks = soup.find(id = "bodyContent").find_all('a')
    
    random.shuffle(allLinks)

    linkToScrape = 0

    for link in allLinks:
        if link['href'].find("/wiki/") == -1: 
            continue

        linkToScrape  = link
        break


    scrapeWikiArticle('https://en.wikipedia.org' + linkToScrape['href'] )
scrapeWikiArticle('https://en.wikipedia.org/wiki/web_scraping')       