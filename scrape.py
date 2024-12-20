from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import json

now = datetime.now()

with open("books/list_cache.json", "r") as books_cache:
    try:
        cache = json.load(books_cache)
    except json.decoder.JSONDecodeError:
        print("The cache is empty or does not exist.")
        cache = {}
        
# Moby Dick Project Gutenberg
url = "https://www.gutenberg.org/cache/epub/15/pg15-images.html"


# Send request if text not in cache
def requesting_web(url):
    
    print("Getting content from web...")
    result = requests.get(url)
    result.encoding = "utf-8"
    if result.status_code == 200: # All is well
        return result
    
    if result.status_code == 503: # The servers are down
        raise ConnectionError("HTTP 503 - Service Unavailable")
    
    # if result.status_code == 404: # Url not found
    #     raise Exception("404 Not Found")
    
    result.raise_for_status()
    
# Extract text
def clean_up(html_content):
    soup = BeautifulSoup(html_content.text, "lxml")
    # Grab title of the book
    title_tag = soup.find("meta", attrs={"name": "dc.title"})
    title = title_tag["content"]

    print(title)
    soup_content = soup.find_all("div", class_ = "chapter")

    # TBFixed
    # a_tag = soup.find("h1")
    # b_tag = soup.find(id="pg-footer")

    # content = []
    # for sibling in a_tag.find_next_siblings():
    #     if sibling == b_tag:
    #         break
    #     content.append(str(sibling))
    
    book = []
    for chapter in soup_content:
        chapter = chapter.text.strip()
        book.append(str(chapter))

    return "".join(book)

def get_book(url):
    print("Content loading...")
    if url not in cache:
        html_content = requesting_web(url)
        cache[url] = clean_up(html_content)

if __name__ == "__main__":
    print(now.strftime("%H:%M:%S"))
    get_book(url)
    
    with open("books/list_cache.json", "w") as books_cache:
        books_cache.write(json.dumps(cache))