from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

# BEGIN - Scraping of web page

# END - Scraping of web page
with open("books/list_cache.json", "r") as books_cache:
    try:
        cache = json.load(books_cache)
    except json.decoder.JSONDecodeError:
        cache = {}
        print("The cache is empty.")

moby_dick = list(cache.items())[0]

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    words = [token.lower() for token in tokens if token.lower().islower()] # Convert to lower case and remove punctuation tokens

    return words

# Filter stopwords
def filter_stopwords(words):
    stop_words = set(stopwords.words('english'))
    if isinstance(words, str):
        words = tokenize(words)

    filtered_list = []
    # Filtering of stop words
    for word in words:
        if word not in stop_words:
            filtered_list.append(word)
    return filtered_list

def stemming_porter(li):
    pstemmer = PorterStemmer()

    result = []
    for word in li:
        word = pstemmer.stem(word)
        result.append(word)

    return result

# Lemmization of words in text
def lemmization(text):
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

    words_list = tokenize(text)
    words_pos_tagged = nltk.pos_tag(words_list)

    wordlist_lemmatized = []
    for word, tag in words_pos_tagged:
        if pos_tagger(tag) == None:
            wordlist_lemmatized.append(word)
        else:
            wordlist_lemmatized.append(lemmatizer.lemmatize(word, pos_tagger(tag)))

    return wordlist_lemmatized

def word_frequency(data):
    if isinstance(data, str):
        data = tokenize(data)

    word_counter = {}
    # Get get the word count for text
    for word in data:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1

    return word_counter

def most_common_words(n, in_dict):
    if not isinstance(in_dict, dict):
        raise TypeError("Not a dictionary")
                                                                    
    common_words = sorted(in_dict.items(), key=lambda item: item[1], reverse=True) # Most common words
    rest_common_words = common_words[:n]
    word = zip(*rest_common_words)

    return list(word)

def word_analysis(sample_text):
    words_of_importance = filter_stopwords(sample_text)
    words_root = stemming_porter(words_of_importance)
    word_freq = word_frequency(words_root)
    words_mc = most_common_words(5, word_freq)

    data = {
        "Word":words_mc[0],
        "Frequency":words_mc[1]
    }

    df = pd.DataFrame(data)

    # word_frequency & most_common words combine?

    print(df.to_string(index=False))

    
if __name__ == "__main__":
    word_analysis(moby_dick)

## Extra: use pandas dataframe for display of word frequency