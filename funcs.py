from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import random
import json
import itertools
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

quote = ""

# Most common words function
def most_common_words(n, sorted_dict):                                                                
    common_words = dict(itertools.islice(sorted_dict.items(), n)) # Most common words

    return list(common_words.keys()) # Get keys of MCW

# Words only used once
def unique_words(in_dict):
    unique_words = []

    for key, value in in_dict.items():
        if value == 1:
            unique_words.append(key)

    return unique_words

# 
def filter_stopwords(text):
    stop_words = set(stopwords.words('english'))

    words = text.split()

    filtered_text = []

    # Filtering of stop words
    for word in words:
        if word.lower() not in stop_words:
            filtered_text.append(word)

# Stemming of words
def stemming_porter(text):
    nltk_words = word_tokenize(text)

    pstemmer = PorterStemmer()

    result = []

    for word in nltk_words:
        if word.isalpha():
            stemmed_word = pstemmer.stem(word)
            result.append(stemmed_word)
        else:
            result.append(word)

    # # Better for DRY?
    # for word in nltk_words:
    #     if word.isalpha():
    #         word = pstemmer.stem(word)
        
    #     result.append(word)


# Comparison of two text
def compare(first_text, second_text):
    text_comparison = [first_text, second_text]
    final_list = []


    for text in text_comparison:
        word_counter = {}

        # Get get the word count for text
        words = text.split()

        for word in words:
            if word in word_counter:
                word_counter[word] += 1
            else:
                word_counter[word] = 1

        # Sorting the word counter by frequency descending
        sorted_word_counter = dict(sorted(word_counter.items(), key=lambda item: item[1], reverse=True))

        mostcommon10 = most_common_words(10, sorted_word_counter)

        final_list.append(mostcommon10)


    return final_list

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

    words_list_crude = nltk.word_tokenize(text)

    # converts each token to lowercase and removes punctuation tokens (such as commas and full stops)
    words_list = [token.lower() for token in words_list_crude if token.islower() or token.isupper()]
    words_pos_tagged = nltk.pos_tag(words_list)


    wordlist_lemmatized = []
    for word, tag in words_pos_tagged:
        if pos_tagger(tag) == None:
            wordlist_lemmatized.append(word)
        else:
            wordlist_lemmatized.append(lemmatizer.lemmatize(word, pos_tagger(tag)))

    return wordlist_lemmatized
