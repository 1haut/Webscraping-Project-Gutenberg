from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import json
import nltk

# Access cached books
with open("books/list_cache.json", "r") as books_cache:
    try:
        cache = json.load(books_cache)
    except json.decoder.JSONDecodeError:
        print("The cache is empty or does not exist.")
        cache = {}

# Moby Dick Project Gutenberg
url = "https://www.gutenberg.org/cache/epub/15/pg15-images.html"

def grab_book(url):
    # Check if book is saved in cache
    if url not in cache:
        print("Getting content from web...")
        result = requests.get(url)
        result.encoding = "utf-8"

        if result.status_code == 200: 
            soup = BeautifulSoup(result.text, "lxml")
            title = soup.find("h1")
            end_book = soup.find(id="pg-footer")

            content = [title.text]
            for chapter in title.find_next_siblings():
                if chapter == end_book:
                    break
                # chapter = chapter.text.strip()
                content.append(str(chapter))
 
            cache[url] = "".join(content)

            if len(content) > 2:
                print("Successfully grabbed book!")

            return cache[url]
        
        result.raise_for_status()

    else:
        if len(cache[url]) > 1:
            print("Retrieving book from cache...")

        return cache[url]
    
def tokenizer(text):
    tokens = nltk.word_tokenize(text)

    words = []

    for token in tokens:
        # Remove trailing punctuation and convert to lowercase
        token = token.rstrip(".").lower()

        # Handle tokens containing "—"
        if "—" in token:
            words.extend(sub_token.lower().rstrip(".") for sub_token in token.split("—"))
            continue

        # Add token if it's a valid word
        if token.isalpha():
            words.append(token)

    return words
    
def most_frequent(url):
    text = cache[url]

    data = tokenizer(text)

    word_counter = {}
    # Get get the word count for text
    for word in data:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1

    common_words = sorted(word_counter.items(), key=lambda item: item[1], reverse=True) # Most common words
    most_frequent_words = common_words[:3]

    # Words only used once
    unique_words = []

    for key, value in common_words:
        if value == 1:
            unique_words.append(key)

    words, occurances = zip(*most_frequent_words)

    data = {
        "Word":words,
        "Frequency":occurances
    }
    df = pd.DataFrame(data)

    r_freq = df.to_string(index=False)
    r_uniq = f"Number of unique words: over {len(unique_words) // 1000} thousand"

    overview = f"Title: Moby Dick \n\nMost frequent words: \n{r_freq} \n\n{r_uniq} \n\n Unique words = {unique_words}"

    with open("analysis_results/simplepy_analysis.txt", "w", encoding="UTF-8") as file:
        file.write(overview)


if __name__ == "__main__":
    print(datetime.now().strftime("%H:%M:%S"))
    grab_book(url)
    most_frequent(url)
    
    # with open("books/list_cache.json", "w") as books_cache:
    #     books_cache.write(json.dumps(cache))

