import pandas as pd
import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

with open("cached_books/cache.json", "r") as books_cache:
    cache = json.load(books_cache)

md_snippet = list(cache.values())[2]

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
        
    if type(words_list) == 'str': # Incase the user did not filter stopwords
        words_list = tokenize(words_list)

    words_list_tagged = nltk.pos_tag(words_list)

    word_list_root_form = []
    for word, tag in words_list_tagged:
        if pos_tagger(tag) == None:
            word_list_root_form.append(word)
        else:
            word_list_root_form.append(lemmatizer.lemmatize(word, pos_tagger(tag)))

    return word_list_root_form

def word_frequency(n, data):
    if isinstance(data, str):
        data = tokenize(data)
    
    word_counter = {}
    # Get get the word count for text
    for word in data:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1

    common_words = sorted(word_counter.items(), key=lambda item: item[1], reverse=True) # Most common words
    most_frequent_words = common_words[:n]

    return dict(most_frequent_words)

def display_dataframe(info):
    if isinstance(info, dict):
        word, occurances = zip(*info.items())

    if isinstance(info, tuple):
        pass

    data = {
        "Word":word,
        "Frequency":occurances
    }
    df = pd.DataFrame(data)

    print(df.to_string(index=False))

if __name__ == "__main__":
    text_words = filter_stopwords(md_snippet)  # Optional, but recommended

    # Optional
    # # Pick one or the other, or none at all
    # root_words = stemming_porter(text_words)
    root_words = lemmization(text_words)

    most_common_words = word_frequency(5, root_words)

    display_dataframe(most_common_words)  # Optional










