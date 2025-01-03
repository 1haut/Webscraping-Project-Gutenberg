# Webscraping Project Gutenberg

This is a simple python app for the scraping of books from [Project Gutenberg](https://www.gutenberg.org/) and basic word analysis with the python packages requests and BeautifulSoup

## Getting Started

### Prerequisites
To use this app you need to install:
- [Python](https://www.python.org/downloads/)
- [Pypi](https://pypi.org/)

### Installation & Usage
1. Fork this repository
2. Clone this repository
   ```
   git clone https://github.com/1haut/Webscraping-Project-Gutenberg.git
   ```
3. Install the required packages
   ```
   pip install requests beautifulsoup4 nltk
   ```
4. Enter the url of the web version of the book at the top of the program, and run the file
   ```python
   # A Simple Soul by Gustave Flaubert
   url = 'https://www.gutenberg.org/cache/epub/1253/pg1253-images.html'
   ```
5. For analysis of the book, keep the url used in the scraping, enter it in the url variable, and run the file
