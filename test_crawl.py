import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html

class TestCrawl(unittest.TestCase):

    # normalize_url unit tests

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

    # get_heading_from_html unit test

    def test_get_heading_from_html(self):
        input_body = '<html><body><h1>Test Title</h1></body></html>'
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_html_with_h1(self):
        input_body = '<html><body><h1>Main Title</h1></body></html>'
        actual = get_heading_from_html(input_body)
        expected = "Main Title"
        self.assertEqual(actual, expected)

    def test_html_with_h2_only(self):
        input_body = '<html><body><h2>Secondary Title</h2></body></html>'
        actual = get_heading_from_html(input_body)
        expected = "Secondary Title"
        self.assertEqual(actual, expected)
    
    def test_html_with_both(self):
        input_body = '<html><body><h1>Main Title</h1><h2>Secondary Title</h2></body></html>'
        actual = get_heading_from_html(input_body)
        expected = "Main Title"
        self.assertEqual(actual, expected)

    def test_html_with_neither(self):
        input_body = '<html><body><p>Just a paragraph</p></body></html>'
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_html_empty_body(self):
        input_body = '<html><body></body></html>'
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_html_nested(self):
        input_body = '<html><body><h1>Main <span>Title</span></h1></body></html>'
        actual = get_heading_from_html(input_body)
        expected = "Main Title"
        self.assertEqual(actual, expected)
    
    def test_multiple_h1(self):
        input_body = '<html><body><h1>First</h1><h1>Second</h1></body></html>'
        actual = get_heading_from_html(input_body)
        expected = "First"
        self.assertEqual(actual, expected)

    def test_html_h2_before_h1(self):
        input_body = '<html><body><h2>Secondary</h2><h1>Main</h1></body></html>'
        actual = get_heading_from_html(input_body)
        expected = "Main"
        self.assertEqual(actual, expected)

    # get_first_paragraph_from_html

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_html_with_p(self):
        input_body = "<html><body><p>This is the first paragraph.</p></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = "This is the first paragraph."
        self.assertEqual(actual, expected)

    def test_html_multiple_p(self):
        input_body = "<html><body><p>First paragraph.</p><p>Second paragraph.</p></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = "First paragraph."
        self.assertEqual(actual, expected)

    def test_html_no_p(self):
        input_body = "<html><body><h1>Just a title</h1></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_html_empty_body(self):
        input_body = "<html><body></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_html_nested_p(self):
        input_body = "<html><body><p>This has <strong>bold</strong> and <em>italic</em> text.</p></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = "This has bold and italic text."
        self.assertEqual(actual, expected)

    def test_html_p_empty_tag(self):
        input_body = "<html><body><p></p></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_html_p_in_div(self):
        input_body = "<html><body><div><p>Paragraph inside a div.</p></div></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = "Paragraph inside a div."
        self.assertEqual(actual, expected)

    def test_html_p_malformed(self):
        input_body = "<html><body><p>Unclosed paragraph<div>Next element</div></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = "Unclosed paragraph Next element"
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()