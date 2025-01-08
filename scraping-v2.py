from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import json

# Access cached book
with open("books/list_cache.json", "r") as books_cache:
    try:
        cache = json.load(books_cache)
    except json.decoder.JSONDecodeError:
        print("The cache is empty or does not exist.")
        cache = {}

# Moby Dick Project Gutenberg
# url = "https://www.gutenberg.org/cache/epub/15/pg15-images.html"

url = 'https://httpstat.us/503'

url = 'https://www.gutenberg.org/cache/epub/12122/pg12122-images.html'

def grab_book(url):
    # Check if book is saved in cache
    if url not in cache:
        print("Getting content from web...")
        result = requests.get(url)
        result.encoding = "utf-8"

        if result.status_code == 200: # All is well
            soup = BeautifulSoup(result.text, "lxml")
            title = soup.find("h1") # Title
            end_book = soup.find(id="pg-footer")

            content = []
            for chapter in title.find_next_siblings():
                if chapter == end_book:
                    break
                chapter = chapter.text.strip()
                content.append(str(chapter))

            text = "".join(content)

            cache[url] = text
            # cache[url] = "".join(content)
        
            if len(text) > 10000:
                print("Successfully grabbed book!")

            # return cache[url]
            return text
        
        result.raise_for_status()

    else:
        return cache[url]
        

if __name__ == "__main__":
    print(datetime.now().strftime("%H:%M:%S"))
    grab_book(url)
    
    with open("cached_books/cache.json", "w") as books_cache:
        books_cache.write(json.dumps(cache))