from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import json
import nltk
import time
import csv
from random import randrange
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import wordnet

# Access cached book
with open("books/list_cache.json", "r") as books_cache:
    try:
        cache = json.load(books_cache)
    except json.decoder.JSONDecodeError:
        print("The cache is empty or does not exist.")
        cache = {}

def search_book():
    with open("Webscraping-Project-Gutenberg/pguterberg/pg_catalog.csv", encoding="UTF-8") as csv_file:
        reader = csv.DictReader(csv_file)
        
        result_dict = {}

        # Keep prompting the user for a search term until there are results
        while not result_dict:
            search_term = input("Search book here: ").strip()

            # Reset the dictionary for each new search
            result_dict = {}

            for row in reader:
                if ((search_term.lower() in row['Authors'].lower() or search_term.lower() in row['Title'].lower())
                    and row['Type'] == 'Text'
                    and row['Language'] == 'en'):

                    authors = str(row['Authors'].split(";")[0])
                    for num in "1234567890":
                        authors = authors.replace(num, "")
                    authors = authors.rstrip(",- ")

                    result_dict[row['Text#']] = f"{row['Title']} by {authors}"
                    print(f"[{row['Text#']}] {row['Title']} by {authors}")

            if not result_dict:
                print("No results found. Please try again.")

        # Get ebook numbers
        ebook_numbers = list(result_dict)

        # Prompt user to choose a valid book
        choice = input("Choose a book: ")
        while choice not in ebook_numbers:
            print("Sorry, but this choice is invalid, please enter the ebook number of your preferred book.")
            time.sleep(0.5)
            choice = input("Choose a book: ")

        print(f"You've chosen {result_dict[choice]}. ")
        
        return (f"https://www.gutenberg.org/cache/epub/{choice}/pg{choice}-images.html", result_dict[choice])

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
    
def tokenizer(text):
    nltk.download('punkt_tab')

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

def frequency_analysis(list_info):
    word_counter = {}
    # Get get the word count for text
    for word in list_info:
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

    words, occurences = zip(*most_frequent_words)

    # Present most frequent words in a dataframe
    data = {
        "Word":words,
        "Frequency":occurences
    }
    df = pd.DataFrame(data)
    df_noindex = df.to_string(index=False)

    # List a sample of 20 unique words
    num_unique_words = len(unique_words)
    random_index = randrange(0, num_unique_words - 20)
    sample_unique_words = unique_words[random_index:random_index + 20]
    
    analysis = f"Most frequent words:\n{df_noindex}\n\nNumber of unique words: {num_unique_words}\n\nSample of unique words:  {sample_unique_words}\n\n"
    return analysis
    

def filter_stopwords(words):
    # Download a list of stopwords if does not exist
    nltk.download('stopwords')
 
    stop_words = set(stopwords.words('english'))

    # Tokenize a text
    if isinstance(words, str):
        words = tokenizer(words)

    filtered_list = []
    # Filtering of stop words
    for word in words:
        if word not in stop_words:
            filtered_list.append(word)

    return filtered_list

def stemming_porter(data):
    if isinstance(data, str):
        data = tokenizer(data)
    
    pstemmer = PorterStemmer()

    list_stemmed = []
    for word in data:
        word = pstemmer.stem(word)
        list_stemmed.append(word)

    return list_stemmed

def lemmatization(words_list):
    # Downloads a word tagger if it does not exist
    nltk.download('averaged_perceptron_tagger_eng')
    nltk.download('wordnet')

    # Initialize Lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Handle string argument
    if isinstance(words_list, str):
        words_list = tokenizer(words_list)

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

    words_list_tagged = nltk.pos_tag(words_list)

    word_list_root_form = []
    for word, tag in words_list_tagged:
        if pos_tagger(tag) == None:
            word_list_root_form.append(word)
        else:
            word_list_root_form.append(lemmatizer.lemmatize(word, pos_tagger(tag)))

    return word_list_root_form

if __name__ == "__main__":
    print(datetime.now().strftime("%H:%M:%S"))
    url, book_title = search_book()
    book_text = grab_book(url)

    # Save book in cache
    with open("cached_books/cache.json", "w") as books_cache:
        books_cache.write(json.dumps(cache))

    # Analyze book text filtering stopwords 
    stopwords_list = filter_stopwords(book_text)
    stopwords_analysis = "Stopword Analysis \n\n" + frequency_analysis(stopwords_list)

    # Analyze book text filtering stopwords and stemming words
    stemmed_stopwords_list = stemming_porter(stopwords_list)
    ssl_analysis = "Stemming Analysis \n\n" + frequency_analysis(stemmed_stopwords_list)

    # Analyze book text filtering stopwords and lemmatizing words
    lemmatized_stopword_list = lemmatization(stopwords_list)
    lsl_analysis = "Lemmatization Analysis \n\n" +  frequency_analysis(lemmatized_stopword_list)

    with open("Webscraping-Project-Gutenberg/analysis_results/base_analysis.txt", "w") as analysis_file:
        analysis_file.write(stopwords_analysis + ssl_analysis + lsl_analysis)