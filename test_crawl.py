import unittest
from crawl import normalize_url

class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    
    def test_normalize_url_two(self):
        input_url = "http://www.google.com/"
        actual = normalize_url(input_url)
        expected = "www.google.com"
        self.assertEqual(actual, expected)

    def test_normalize_url_three(self):
        input_url = "http://www.facebook.com/login/rhys/"
        actual = normalize_url(input_url)
        expected = "www.facebook.com/login/rhys"
        self.assertEqual(actual, expected)

    def test_normalize_url_four(self):
        input_url = "www.google.com"
        actual = normalize_url(input_url)
        expected = "www.google.com"
        self.assertEqual(actual, expected)

    def test_normalize_url_five(self):
        input_url = "http://www.google.com/login/gage/login/login/"
        actual = normalize_url(input_url)
        expected = "www.google.com/login/gage/login/login"
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()