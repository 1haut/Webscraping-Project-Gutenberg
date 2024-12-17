import unittest
from scrape import requesting_web


class TextScraping(unittest.TestCase):
    def test_url_req(self):
       """
       Test url for a valid website
       """
       TEST_URL = "https://example.com"
       page_content = requesting_web(TEST_URL)
       self.assertEqual(page_content.status_code, 200)

    def test_raise_for_status(self):
        TEST_URL = "https://example.com"
        page_content = requesting_web(TEST_URL)
        self.assertEqual(page_content.raise_for_status(), None)

    def test_faulty_site(self):
        TEST_URL = "https://google.com/not"
        page_content = requesting_web(TEST_URL)
        self.assertNotEqual(page_content.raise_for_status(), None)


if __name__ == "__main__":
    unittest.main(verbosity=2)