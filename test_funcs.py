import unittest
import scrape


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


if __name__ == "__main__":
    unittest.main(verbosity=2)