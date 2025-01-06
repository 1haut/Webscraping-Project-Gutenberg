# Wordcloud analysis

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json
import numpy as np
import functools
import random
import timeit

with open("cached_books/cache.json", "r") as books_cache:
    cache = json.load(books_cache)

text_snippet = cache["md_extract"]

def display_wordcloud():
    wordcloud = WordCloud().generate(text_snippet)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

# Visualize with graphs
def add_graphs():
    frequency_dict_test = {'sak pase': 20, 'merhaba': 14, 'guten tag': 13, 'hola': 12, 'hello': 11, 'hallois': 5}

    word, occurances = zip(*frequency_dict_test.items())

    fig, ax = plt.subplots()

    ax.barh(word, occurances, height = 0.4)
    ax.invert_yaxis()
    ax.set_title("Most common greetings")
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Greeting")

    plt.show()

# Test LRU-caching
@functools.lru_cache(maxsize=1)
def speed_test():
    greetings = ["hello", "hei", "hola", "bonjour", "guten tag", "merhaba", "ni hao", "namaste", "privyet", "assalaam aleikum"]

    li = []

    for _ in range(1000000):
        greeting = random.choice(greetings)
        li.append(greeting)

    return li

# Test api-key
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API-KEY")

if not api_key:
    raise Exception("Key not reached...")

word = "whale"



