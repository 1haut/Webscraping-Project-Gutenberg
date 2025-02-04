import unittest
import simple_v2
from unittest.mock import patch
from io import StringIO

# class TestScraping(unittest.TestCase):
#     def test_scraping_webpage(self):
#         TEST_URL = "https://example.com"
#         scrape_content = simple_v2.grab_book(TEST_URL)
#         self.assertIn("Example", scrape_content)

#     def test_content(self):
#         TEST_URL = "https://example.com"
#         scrape_content = simple_v2.grab_book(TEST_URL)
#         self.assertGreater(len(scrape_content), 100)

#     def test_faulty_site(self):
#         TEST_URL = "https://opensource.org/not"
#         with self.assertRaises(Exception):
#             simple_v2.grab_book(TEST_URL)

#     def test_service_unavailable(self):
#         TEST_URL = "https://httpstat.us/503"
#         with self.assertRaises(Exception):
#             simple_v2.grab_book(TEST_URL)

#     def test_url_in_cache(self):
#         # Moby Dick
#         TEST_URL = "https://www.gutenberg.org/cache/epub/15/pg15-images.html"
#         self.assertIn(TEST_URL, simple_v2.cache)

#     def test_url_not_in_cache(self):
#         # A Doll's House
#         TEST_URL = "https://www.gutenberg.org/cache/epub/2542/pg2542-images.html"
#         self.assertNotIn(TEST_URL, simple_v2.cache)

# class TestAnalysis(unittest.TestCase):
#     def test_tokenizer(self):
#         TEST_STRING = "He who conquers himself is the mightiest warrior. (Confucius)"
#         tokens = simple_v2.tokenizer(TEST_STRING)
#         self.assertEqual(len(tokens), 9)

#     def test_stemming(self):
#         stemming_list = ["program","programming","programer","programs","programmed"]
#         result = simple_v2.stemming_porter(stemming_list)
#         for word in result:
#             with self.subTest(word=word):
#                 self.assertEqual(word, "program")

#     def test_lemmatization(self):
#         word_inflections = ["exchange", "exchanged", "exchanging", "exchanges"]
#         words_lemmatized = simple_v2.lemmatization(word_inflections)
#         for word in words_lemmatized:
#             with self.subTest(word=word):
#                 self.assertEqual(word, "exchange")

#     def test_stopword_filtering(self):
#         TEST_STRING = "The Lion, the Witch and the Wardrobe"
#         list_no_stopwords = simple_v2.filter_stopwords(TEST_STRING)
#         self.assertEqual(len(list_no_stopwords), 3)

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.sample_csv = StringIO(
            """Text#,Type,Issued,Title,Language,Authors,Subjects,LoCC,Bookshelves
1,Text,1971-12-01,The Declaration of Independence of the United States of America,en,"Jefferson, Thomas, 1743-1826","United States -- History -- Revolution, 1775-1783 -- Sources; United States. Declaration of Independence",E201; JK,Politics; American Revolutionary War; United States Law; Browsing: History - American; Browsing: History - Warfare; Browsing: Politics
2,Text,1972-12-01,"The United States Bill of Rights
The Ten Original Amendments to the Constitution of the United States",en,United States,Civil rights -- United States -- Sources; United States. Constitution. 1st-10th Amendments,JK; KF,Politics; American Revolutionary War; United States Law; Browsing: History - American; Browsing: Law & Criminology; Browsing: Politics
3,Text,1973-11-01,John F. Kennedy's Inaugural Address,en,"Kennedy, John F. (John Fitzgerald), 1917-1963",United States -- Foreign relations -- 1961-1963; Presidents -- United States -- Inaugural addresses,E838,Browsing: History - American; Browsing: Politics
4,Text,1973-11-01,"Lincoln's Gettysburg Address
Given November 19, 1863 on the battlefield near Gettysburg, Pennsylvania, USA",en,"Lincoln, Abraham, 1809-1865","Consecration of cemeteries -- Pennsylvania -- Gettysburg; Soldiers' National Cemetery (Gettysburg, Pa.); Lincoln, Abraham, 1809-1865. Gettysburg address",E456,US Civil War; Browsing: History - American; Browsing: Politics
5,Text,1975-12-01,The United States Constitution,en,United States,United States -- Politics and government -- 1783-1789 -- Sources; United States. Constitution,JK; KF,United States; Politics; American Revolutionary War; United States Law; Browsing: History - American; Browsing: Law & Criminology; Browsing: Politics
6,Text,1976-12-01,Give Me Liberty or Give Me Death,en,"Henry, Patrick, 1736-1799","Speeches, addresses, etc., American; United States -- Politics and government -- 1775-1783 -- Sources; Virginia -- Politics and government -- 1775-1783 -- Sources",E201,American Revolutionary War; Browsing: History - American; Browsing: History - Warfare; Browsing: Politics
7,Text,1977-12-01,The Mayflower Compact,en,,"Massachusetts -- History -- New Plymouth, 1620-1691 -- Sources; Pilgrims (New Plymouth Colony); Mayflower Compact (1620)",F001,Browsing: History - American
8,Text,1978-12-01,Abraham Lincoln's Second Inaugural Address,en,"Lincoln, Abraham, 1809-1865",United States -- Politics and government -- 1861-1865; Presidents -- United States -- Inaugural addresses,E456,US Civil War; Browsing: History - American; Browsing: Politics
9,Text,1979-12-01,Abraham Lincoln's First Inaugural Address,en,"Lincoln, Abraham, 1809-1865",United States -- Politics and government -- 1861-1865; Presidents -- United States -- Inaugural addresses,E456,US Civil War; Browsing: History - American; Browsing: Politics
"""
        )

    @patch('builtins.input', side_effect=["lincoln", "8"])
    def test_input_successful(self, mock_input):
        result = simple_v2.search_book(self.sample_csv)
        book_url = result[0]
        book_title = result[1]
        self.assertEqual(book_url, "https://www.gutenberg.org/cache/epub/8/pg8-images.html")
        self.assertTrue(book_title.endswith("Lincoln, Abraham"))

    @patch('builtins.input', side_effect=["lincoln", "1", "8"])
    def test_input_wrong_book_number(self, mock_input):
        result = simple_v2.search_book(self.sample_csv)
        book_url = result[0]
        book_title = result[1]
        self.assertEqual(book_url, "https://www.gutenberg.org/cache/epub/8/pg8-images.html")
        self.assertTrue(book_title.endswith("Lincoln, Abraham"))

    @patch('builtins.input', side_effect=["lincoln", "u", "8"])
    def test_input_fail_to_enter_book_number(self, mock_input):
        result = simple_v2.search_book(self.sample_csv)
        book_url = result[0]
        book_title = result[1]
        self.assertEqual(book_url, "https://www.gutenberg.org/cache/epub/8/pg8-images.html")
        self.assertTrue(book_title.endswith("Lincoln, Abraham"))

    
if __name__ == "__main__":
    unittest.main(verbosity=2)