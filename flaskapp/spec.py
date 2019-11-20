import unittest
import server


class TestRunner(unittest.TestCase):
    def test_scraping_show_with_movie_preference(self):
        scraper = server.WebScraper()
        with self.assertRaises(Exception) as context:
            scraper.scrape("jackass")
        self.assertTrue("The correct tv show was not found. Try revising your search or adding tv at the end." in str(context.exception))
    def test_scraping_show_with_tv_show_specification(self):
        scraper = server.WebScraper()
        try:
            scraper.scrape("jackass tv")
        except Exception:
            self.fail("Web scraper did not pick up a tv search!")
    def fails_on_movie_search(self):
        scraper = server.WebScraper()
        with self.assertRaises(Exception) as context:
            scraper.scrape("Pirates of the Carribean")
        self.assertTrue("The correct tv show was not found. Try revising your search or adding tv at the end." in str(context.exception))
    def runs_successfully_with_show_with_synopsis(self):
        scraper = server.WebScraper()
        try:
            scraper.scrape("game of thrones")
        except Exception:
            self.fail("Web scraper did not get a synopsis")
    def runs_successfully_with_show_with_no_synopsis(self):
        scraper = server.WebScraper()
        try:
            scraper.scrape("greys anatomy")
        except Exception:
            self.fail("Web scraper did not get a synopsis")

if __name__ == '__main__':
    unittest.main()