# %%
import unittest
import scraper_class

class TestScraperClass(unittest.TestCase):
    def setUp(self):
        self.scraper = scraper_class.ScraperClass

    def test_cookie_ad_clicker(self):
        self.assertEqual(self.scraper.cookie_ad_clicker(self), 1)

    def test_url_link_scraper(self):
        self.assertEqual(self.scraper.url_link_scraper(self), "https://crypto.com/price/bitcoin")
       
   
if __name__ == "__main__":
    unittest.main()

# %%
