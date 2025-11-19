import unittest
from src.seo_analyzer import SEOAnalyzer

class TestSEOAnalyzer(unittest.TestCase):
    def test_analyze_valid_page(self):
        page_data = {
            "title": "A Perfect Title for SEO",
            "meta_description": "This is a perfect meta description that is long enough to be good but not too long.",
            "h1": "Main Heading",
            "load_time_ms": 500
        }
        issues = SEOAnalyzer.analyze(page_data)
        self.assertEqual(len(issues), 0)

    def test_missing_title(self):
        page_data = {
            "title": None,
            "meta_description": "This is a valid meta description that is definitely longer than fifty characters to pass the check.",
            "h1": "Valid H1",
            "load_time_ms": 500
        }
        issues = SEOAnalyzer.analyze(page_data)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['issue_type'], 'missing_title')

    def test_short_title(self):
        page_data = {
            "title": "Short",
            "meta_description": "This is a valid meta description that is definitely longer than fifty characters to pass the check.",
            "h1": "Valid H1",
            "load_time_ms": 500
        }
        issues = SEOAnalyzer.analyze(page_data)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['issue_type'], 'short_title')

    def test_long_title(self):
        page_data = {
            "title": "A" * 70,
            "meta_description": "This is a valid meta description that is definitely longer than fifty characters to pass the check.",
            "h1": "Valid H1",
            "load_time_ms": 500
        }
        issues = SEOAnalyzer.analyze(page_data)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['issue_type'], 'long_title')

    def test_missing_meta_desc(self):
        page_data = {
            "title": "Valid Title",
            "meta_description": None,
            "h1": "Valid H1",
            "load_time_ms": 500
        }
        issues = SEOAnalyzer.analyze(page_data)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['issue_type'], 'missing_meta_desc')

    def test_slow_load_time(self):
        page_data = {
            "title": "Valid Title",
            "meta_description": "This is a valid meta description that is definitely longer than fifty characters to pass the check.",
            "h1": "Valid H1",
            "load_time_ms": 4000
        }
        issues = SEOAnalyzer.analyze(page_data)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['issue_type'], 'slow_load_time')
        self.assertEqual(issues[0]['severity'], 'warning')

    def test_critical_load_time(self):
        page_data = {
            "title": "Valid Title",
            "meta_description": "This is a valid meta description that is definitely longer than fifty characters to pass the check.",
            "h1": "Valid H1",
            "load_time_ms": 7000
        }
        issues = SEOAnalyzer.analyze(page_data)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['issue_type'], 'slow_load_time')
        self.assertEqual(issues[0]['severity'], 'critical')

if __name__ == '__main__':
    unittest.main()
