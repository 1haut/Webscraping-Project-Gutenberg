from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json
import numpy as np
import random
import requests
import nltk
from textblob import TextBlob
from simple_v2 import tokenizer
from dotenv import load_dotenv
import os

nltk.download('brown')
nltk.download('universal_tagset')

# Word visualization with Wordcloud(s)
def display_wordcloud(text):
    wordcloud = WordCloud().generate(text)

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
# @functools.lru_cache(maxsize=1)
def speed_test():
    greetings = ["hello", "hei", "hola", "bonjour", "guten tag", "merhaba", "ni hao", "namaste", "privyet", "assalaam aleikum"]

    li = []

    for _ in range(1000000):
        greeting = random.choice(greetings)
        li.append(greeting)

    return li

# Sentence analysis
def sentiment_tb():

 
    sen_1 = """
For half a century the housewives of Pont-l’Eveque had envied Madame Aubain her servant Felicite.

For a hundred francs a year, she cooked and did the housework, washed, ironed, mended, harnessed the horse, fattened the poultry, made the butter and remained faithful to her mistress—although the latter was by no means an agreeable person.

Madame Aubain had married a comely youth without any money, who died in the beginning of 1809, leaving her with two young children and a number of debts. She sold all her property excepting the farm of Toucques and the farm of Geffosses, the income of which barely amounted to 5,000 francs; then she left her house in Saint-Melaine, and moved into a less pretentious one which had belonged to her ancestors and stood back of the market-place. This house, with its slate-covered roof, was built between a passage-way and a narrow street that led to the river. The interior was so unevenly graded that it caused people to stumble. A narrow hall separated the kitchen from the parlour, where Madame Aubain sat all day in a straw armchair near the window. Eight mahogany chairs stood in a row against the white wainscoting. An old piano, standing beneath a barometer, was covered with a pyramid of old books and boxes. On either side of the yellow marble mantelpiece, in Louis XV. style, stood a tapestry armchair. The clock represented a temple of Vesta; and the whole room smelled musty, as it was on a lower level than the garden.

"""

    blob = TextBlob(sen_1)

    shortest_sentence = longest_sentence = blob.sentences[0]
    wordiest_sentence = (blob.sentences[0], len(tokenizer(str(new_sen))))
    
    for new_sen in blob.sentences[1:]:
        words = tokenizer(str(new_sen))
        if (len(new_sen) < len(shortest_sentence) 
            and len(words) >= 3 
            and new_sen[0].isupper()):
            shortest_sentence = new_sen

        if len(longest_sentence) < len(new_sen):
            longest_sentence = new_sen

        if words > wordiest_sentence[1]:
            wordiest_sentence = (new_sen, words)
    
    print(shortest_sentence)

def avg_length_sentence(text):
    blob = TextBlob(text)
    total = 0

    for new_sen in blob.sentences:
        words = tokenizer(str(new_sen))
        total += len(words)
    
    return total / len(blob.sentences)

def sentence_startswith(text):
    blob = TextBlob(text)

    condition_sentences = []
    for sentence in blob.sentences:
        if sentence.startswith("The"):
            condition_sentences.append(str(sentence))

    return condition_sentences


# Sentiment Analysis

def get_api_key():
    load_dotenv()
    api_key = os.getenv("API-KEY")

    if not api_key:
        raise Exception("Key not reached...")

    return api_key

def dict_lookup(word):
    api_key = get_api_key()
    url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={api_key}"
    resp = requests.get(url)

    if resp.status_code == 200:
        data = resp.json()
        
        text = json.dumps(data, sort_keys=True, indent=4)

        f = open("Webscraping-Project-Gutenberg/exampleword.json", "w")
        f.write(text)
        f.close()

        return text
    
    resp.raise_for_status()

# Grab synonyms
def grab_syns():

    with open("cached_books/temp_cache.json", "r") as file:
        data = json.load(file)

    syns_list = data[0]["meta"]["syns"][0]
    first_five_syns = syns_list[:5]


    print(first_five_syns)



def sentiment_vader():
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    sentences = ["Madame Aubain had married a comely youth without any money, who died in the beginning of 1809, leaving her with two young children and a number of debts."]

    analyzer = SentimentIntensityAnalyzer()
    for sentence in sentences:
        vs = analyzer.polarity_scores(sentence)
        print(vs["compound"])


def word_class_tag():
    

    text = "For half a century the housewives of Pont-l’Eveque had envied Madame Aubain her servant Felicite. For a hundred francs a year, she cooked and did the housework, washed, ironed, mended, harnessed the horse, fattened the poultry, made the butter and remained faithful to her mistress — although the latter was by no means an agreeable person."

    tokens = tokenizer(text)

    tokens_tag = nltk.pos_tag(tokens, tagset="universal")

    word_class = {}
    for token_tag in tokens_tag:
        tag = token_tag[1]
        if tag in word_class:
            word_class[tag] += 1
        else:
            word_class[tag] = 1 


if __name__ == "__main__":
    file = open("Webscraping-Project-Gutenberg/sample_texts/preface.txt", "r")
    text = file.read()

    print(sentence_startswith(text))

    file.close()

    

