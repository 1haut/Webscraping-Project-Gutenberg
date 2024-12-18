import unittest
import scrape
import analysis


class TestScraping(unittest.TestCase):
    def test_url_req(self):
       """
       Test url for a valid website
       """
       TEST_URL = "https://example.com"
       page_content = scrape.requesting_web(TEST_URL)
       self.assertEqual(page_content.status_code, 200)

    def test_raise_for_status(self):
        TEST_URL = "https://example.com"
        page_content = scrape.requesting_web(TEST_URL)
        self.assertEqual(page_content.raise_for_status(), None)

    def test_faulty_site(self):
        with self.assertRaises(Exception):
            TEST_URL = "https://opensource.org/not"
            scrape.requesting_web(TEST_URL)

class TestAnalysis(unittest.TestCase):
    def test_word_frequency_string(self):
        """Word frequency function takes a string argument"""
        s = "The future belongs to those who believe in the beauty of their dreams"
        func = analysis.word_frequency(s)
        self.assertIsInstance(func, dict)

    def test_word_frequency_list(self):
        """Word frequency function takes a list argument"""
        li = ["hello", "hei", "hola", "bonjour", "hei"]
        func = analysis.word_frequency(li)
        self.assertIsInstance(func, dict)

    def test_word_frequency_most_common_word(self):
        li = ["hello", "hei", "hola", "bonjour", "hei"]
        func = analysis.word_frequency(li)
        self.assertEqual(list(func)[0], "hei")

if __name__ == "__main__":
    unittest.main(verbosity=2)