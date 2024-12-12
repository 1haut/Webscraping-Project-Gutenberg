from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import json
import itertools

# current_time = time.ctime(time.time())

# cache = {}

with open("cached_books/cache.json", "r") as books_cache:
    try:
        cache = json.load(books_cache)
    except json.decoder.JSONDecodeError:
        cache = {}
        print("The cache is empty.")


# Moby Dick Project Gutenberg
# url = "https://www.gutenberg.org/cache/epub/15/pg15-images.html"

url = "https://books.toscrape.com/catalogue/soumission_998/index.html"


# Send request if text not in cache
def requesting_web(url):
    print("Getting content from web...")
    result = requests.get(url)
    result.encoding = "utf-8"
    if result.raise_for_status() == None:
        return result.text
    result.raise_for_status()

# Extract text
def clean_up(html_content):
    soup = BeautifulSoup(html_content, "lxml")
    souped_content = soup.find("article", class_ = "product_page")
    paragraph = souped_content.find("p", recursive=False).text
    return paragraph

def get_book(url):
    print("Content loading...")
    if url in cache:
        cache[url]
    else:
        html_content = requesting_web(url)
        cache[url] = clean_up(html_content)
  
get_book(url)

with open("cached_books/cache.json", "w") as books_cache:
    books_cache.write(json.dumps(cache))

print(cache[url])