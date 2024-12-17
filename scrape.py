from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time
import pandas as pd
import json
import itertools

now = datetime.now()

with open("cached_books/cache2.json", "r") as books_cache:
    try:
        cache = json.load(books_cache)
    except json.decoder.JSONDecodeError:
        cache = {}
        print("The cache is empty.")


# Moby Dick Project Gutenberg
url = "https://www.gutenberg.org/cache/epub/15/pg15-images.html"

# url = "https://books.toscrape.com/catalogue/soumission_998/index.html"

# url = "https://openddddddddddsource.org/not"

# Send request if text not in cache
def requesting_web(url):
    try:
        print("Getting content from web...")
        result = requests.get(url)
        result.encoding = "utf-8"
        if result.raise_for_status() == None:
            return result
    except requests.exceptions.HTTPError as httperror:
        print(f"HTTPError: {httperror}")
    except Exception as e:
        # Extract and print only the name of the exception
        print(e.__class__.__name__, e)
    
# Extract text
def clean_up(html_content):
    soup = BeautifulSoup(html_content.text, "lxml")
    # Grab title of the book
    title_tag = soup.find("meta", attrs={"name": "dc.title"})
    title = title_tag["content"]

    print(title)
    soup_content = soup.find_all("div", class_ = "chapter")
    
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
    current_time = now.strftime("%H:%M:%S")
    print(current_time)
    get_book(url)
    
    # with open("cached_books/cache.json", "w") as books_cache:
    #     books_cache.write(json.dumps(cache))