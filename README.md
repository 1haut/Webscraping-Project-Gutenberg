# Webscraping Project Gutenberg

This is a simple python app for the scraping of books from [Project Gutenberg](https://www.gutenberg.org/) and basic word analysis with the python packages [requests](https://requests.readthedocs.io/en/latest/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## Getting Started

### Prerequisites
To use this app you need to install:
- [Python](https://www.python.org/downloads/)
- [Pypi](https://pypi.org/)

## Installation & Usage
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

## Improvements
Since this is a rather basic web scraper, there are tons of ways to improve the code to add more functions, such as:
- Improvement of caching
- More advanced analysis
- Support for other languages than English
- Support for scraping with content loaded by JavaScript/AJAX
- Spoofing of headers
- More advanced string matching for better searching in the catalogue 

## Contributing
If for some reason, you want to contribute to the project, follow these steps:
1. Fork this repository
2. Create a branch `git checkout -b <branch_name>`
3. Make your adjustments and commit them `git commit -m <commit message>`
4. Push your adjustments to the original branch `git push -u origin <project_name>/<local>`
5. Make a pull request
