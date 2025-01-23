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
# from nltk.stem import WordNetLemmatizer, PorterStemmer
# from nltk.tokenize import word_tokenize
# from nltk.corpus import wordnet

book_title = "Dracula by Bram Stoker"

text = """
All day long we seemed to dawdle through a country which was full of beauty of every kind. Sometimes we saw little towns or castles on the top of steep hills such as we see in old missals; sometimes we ran by rivers and streams which seemed from the wide stony margin on each side of them to be subject to great floods. It takes a lot of water, and running strong, to sweep the outside edge of a river clear. At every station there were groups of people, sometimes crowds, and in all sorts of attire. Some of them were just like the peasants at home or those I saw coming through France and Germany, with short jackets and round hats and home-made trousers; but others were very picturesque. The women looked pretty, except when you got near them, but they were very clumsy about the waist. They had all full white sleeves of some kind or other, and most of them had big belts with a lot of strips of something fluttering from them like the dresses in a ballet, but of course there were petticoats under them. The strangest figures we saw were the Slovaks, who were more barbarian than the rest, with their big cow-boy hats, great baggy dirty-white trousers, white linen shirts, and enormous heavy leather belts, nearly a foot wide, all studded over with brass nails. They wore high boots, with their trousers tucked into them, and had long black hair and heavy black moustaches. They are very picturesque, but do not look prepossessing. On the stage they would be set down at once as some old Oriental band of brigands. They are, however, I am told, very harmless and rather wanting in natural self-assertion.
It was on the dark side of twilight when we got to Bistritz, which is a very interesting old place. Being practically on the frontier—for the Borgo Pass leads from it into Bukovina—it has had a very stormy existence, and it certainly shows marks of it. Fifty years ago a series of great fires took place, which made terrible havoc on five separate occasions. At the very beginning of the seventeenth century it underwent a siege of three weeks and lost 13,000 people, the casualties of war proper being assisted by famine and disease.
Count Dracula had directed me to go to the Golden Krone Hotel, which I found, to my great delight, to be thoroughly old-fashioned, for of course I wanted to see all I could of the ways of the country. I was evidently expected, for when I got near the door I faced a cheery-looking elderly woman in the usual peasant dress—white undergarment with long double apron, front, and back, of coloured stuff fitting almost too tight for modesty. When I came close she bowed and said, “The Herr Englishman?” “Yes,” I said, “Jonathan Harker.” She smiled, and gave some message to an elderly man in white shirt-sleeves, who had followed her to the door. He went, but immediately returned with a letter
"""

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
    

def filter_stopwords(words):
    # Download a list of stopwords if does not exist
    nltk.download('stopwords')
 
    stop_words = set(stopwords.words('english'))
    if isinstance(words, str):
        words = tokenizer(words)

    filtered_list = []
    # Filtering of stop words
    for word in words:
        if word not in stop_words:
            filtered_list.append(word)
    return filtered_list

# def stemming_porter(data):
#     if isinstance(data, str):
#         data = tokenizer(data)
    
#     pstemmer = PorterStemmer()

#     result = []
#     for word in data:
#         word = pstemmer.stem(word)
#         result.append(word)

#     return result

# def lemmization(words_list):
#     # Downloads a word tagger if it does not exist
#     nltk.download('averaged_perceptron_tagger')

#     # Initialize Lemmatizer
#     lemmatizer = WordNetLemmatizer()

#     # Tag each word in categories
#     def pos_tagger(nltk_tag):
#         if nltk_tag.startswith('J'):
#             return wordnet.ADJ
#         elif nltk_tag.startswith('V'):
#             return wordnet.VERB
#         elif nltk_tag.startswith('N'):
#             return wordnet.NOUN
#         elif nltk_tag.startswith('R'):
#             return wordnet.ADV
#         else:          
#             return None
        
#     if isinstance(words_list, str): # Incase the user did not filter stopwords
#         words_list = tokenizer(words_list)

#     words_list_tagged = nltk.pos_tag(words_list)

#     word_list_root_form = []
#     for word, tag in words_list_tagged:
#         if pos_tagger(tag) == None:
#             word_list_root_form.append(word)
#         else:
#             word_list_root_form.append(lemmatizer.lemmatize(word, pos_tagger(tag)))

#     return word_list_root_form
    
# def most_frequent(url):
    data = tokenizer(text)
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

def frequency_from_list(list_info):
    word_counter = {}
    # Get get the word count for text
    for word in list_info:
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

    words, occurences = zip(*most_frequent_words)

    data = {
        "Word":words,
        "Frequency":occurences
    }
    df = pd.DataFrame(data)

    title = book_title
    word_prevalence = df.to_string(index=False)
    num_unique_words = len(unique_words)
    sample_index = randrange(0, len(unique_words) - 20)
    sample_unique_words = unique_words[sample_index:sample_index + 20]



    analysis = f"Title: {title}\n\nMost frequent words:\n{word_prevalence}\n\nNumber of unique words: {num_unique_words}\n\nSample of unique words:  {sample_unique_words}"
    print(analysis)

word_list = filter_stopwords(text)

frequency_from_list(word_list)

