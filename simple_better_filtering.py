from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

# Access cached book
with open("books/list_cache.json", "r") as books_cache:
    try:
        cache = json.load(books_cache)
    except json.decoder.JSONDecodeError:
        print("The cache is empty or does not exist.")
        cache = {}

# Moby Dick Project Gutenberg
url = "https://www.gutenberg.org/cache/epub/15/pg15-images.html"

def choose_book():
    user_input = input("Insert the Project Gutenberg url for your chosen book OR a valid Project Gutenberg EBook-No: ")

    while not (user_input.isnumeric() and 0 < int(user_input) < 75000 
           or (user_input.endswith(".html") and ("gutenberg.org" in user_input))):
        print("Sorry, that input is invalid, please try again.")
        user_input = input("Insert the Project Gutenberg url for your chosen book OR a valid Project Gutenberg EBook-No: ")

    if user_input.isnumeric():
        inner_url = f"https://www.gutenberg.org/cache/epub/{user_input}/pg{user_input}-images.html" 
    else:
        inner_url = user_input

    return inner_url


def grab_book(url):
    # Check if book is saved in cache
    if url not in cache:
        print("Getting content from web...")
        result = requests.get(url)
        result.encoding = "utf-8"

        if result.status_code == 200: # All is well
            soup = BeautifulSoup(result.text, "lxml")
            title = soup.find("h1")
            end_book = soup.find(id="pg-footer")

            content = [title]
            for chapter in title.find_next_siblings():
                if chapter == end_book:
                    break
                chapter = chapter.text.strip()
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
    
def tokenize(text):
    tokens = nltk.word_tokenize(text)
    words = [token.lower() for token in tokens if token.lower().islower()] # Convert to lower case and remove punctuation tokens

    return words

def filter_stopwords(words):
    # Download a list of stopwords if does not exist
    nltk.download('stopwords')
 
    stop_words = set(stopwords.words('english'))
    if isinstance(words, str):
        words = tokenize(words)

    filtered_list = []
    # Filtering of stop words
    for word in words:
        if word not in stop_words:
            filtered_list.append(word)
    return filtered_list

def stemming_porter(data):
    if isinstance(data, str):
        data = tokenize(data)
    
    pstemmer = PorterStemmer()

    result = []
    for word in data:
        word = pstemmer.stem(word)
        result.append(word)

    return result

def lemmization(words_list):
    # Downloads a word tagger if it does not exist
    nltk.download('averaged_perceptron_tagger')

    # Initialize Lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Tag each word in categories
    def pos_tagger(nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:          
            return None
        
    if isinstance(words_list, str): # Incase the user did not filter stopwords
        words_list = tokenize(words_list)

    words_list_tagged = nltk.pos_tag(words_list)

    word_list_root_form = []
    for word, tag in words_list_tagged:
        if pos_tagger(tag) == None:
            word_list_root_form.append(word)
        else:
            word_list_root_form.append(lemmatizer.lemmatize(word, pos_tagger(tag)))

    return word_list_root_form
    
def most_frequent(url):
    text = cache[url]

    data = tokenize(text)
    data = filter_stopwords(data)
    data = lemmization(data)

    word_counter = {}
    # Get get the word count for text
    for word in data:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1

    common_words = sorted(word_counter.items(), key=lambda item: item[1], reverse=True) # Most common words
    most_frequent_words = common_words[:3]


    # # Words only used once
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

    overview = f"Title: Moby Dick \n\nMost frequent words: \n{r_freq} \n\n{r_uniq}"

    print(overview)

    with open("analysis_results/simplepy_analysis.txt", "w") as file:
        file.write(overview)


if __name__ == "__main__":
    print(datetime.now().strftime("%H:%M:%S"))
    url = choose_book()
    grab_book(url)
    most_frequent(url)
    
    # with open("books/list_cache.json", "w") as books_cache:
    #     books_cache.write(json.dumps(cache))