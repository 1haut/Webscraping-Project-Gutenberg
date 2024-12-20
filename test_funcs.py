import unittest
import scrape
import analysis

from unittest.mock import patch


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

    @patch("scrape.requests.get")
    def test_change_status_code(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 503

        with self.assertRaises(ConnectionError):
            scrape.requesting_web("url")



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

    # def test_word_frequency_most_common_word(self):
    #     li = ["hello", "hei", "hola", "bonjour", "hei"]
    #     func = analysis.word_frequency(li)
    #     self.assertEqual(list(func)[0], "hei")

    def test_tokenization(self):
        s = "I'm not upset that you lied to me, I'm upset that from now on I can't believe you."
        result = analysis.tokenize(s)
        self.assertEqual(len(result), 21)

if __name__ == "__main__":
    unittest.main(verbosity=2)