from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

url = ""
result = requests.get(url)

html_content = result.text

soup = BeautifulSoup(html_content, "lxml")