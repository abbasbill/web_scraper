import requests
import random
from bs4 import BeautifulSoup as bs

# Wikipedia requires a proper User-Agent header
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def scrapeWikiArticle(url, depth=0, max_depth=5):
    if depth > max_depth:
        print("Reached max depth. Stopping.")
        return

    print(f"\nScraping ({depth}): {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return

    soup = bs(response.content, 'html.parser')

    # Find title (works with current Wikipedia structure)
    title = soup.find(id='firstHeading')
    if not title:
        title = soup.find('h1')
    print("Title:", title.text if title else "No title found")

    # Find main content area (mw-parser-output is the current class)
    content = soup.find('div', {'class': 'mw-parser-output'})
    if not content:
        content = soup.find(id="bodyContent")  # fallback for older structure
    
    if not content:
        print("Could not find content area. Stopping this branch.")
        return

    allLinks = content.find_all('a')
    random.shuffle(allLinks)

    for link in allLinks:
        if not link.has_attr('href'):
            continue
        href = link['href']
        if href.startswith("/wiki/") and ":" not in href:   # avoid special pages
            next_url = "https://en.wikipedia.org" + href
            scrapeWikiArticle(next_url, depth+1, max_depth)
            break

scrapeWikiArticle("https://en.wikipedia.org/wiki/Web_scraping")
