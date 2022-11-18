# %%
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time


driver = webdriver.Chrome()
URL = "https://crypto.com/price/ethereum"
website = driver.get(URL)


class ScraperClass:
    def __init__(self, website):
        self.website = website

    def cookie_ad_clicker(self):
        delay = 10
        try:    
            time.sleep(4)
            driver.execute_script("window.scrollTo(0, 250)")
            time.sleep(2)
            decline_cookies_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-reject-all-handler"]')))
            decline_cookies_button.click()
            

        except TimeoutException:
            print("Loading took too much time.")

        try:
            time.sleep(1)
            driver.find_element(by=By.XPATH, value='//*[@id="tabs-:R2hj9aklt6:--tab-1"]').click()
            
            time.sleep(2)
            driver.find_element(by=By.XPATH, value='//*[@href="/price"]').click()
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, 500)")
            time.sleep(2)
            self.url_link_scraper()
            
            
        except:
            pass

    def url_link_scraper(self):
        links = []
        links = links + driver.find_elements(by=By.TAG_NAME, value="a")
        
        for index in links[29:79]:
            links = index.get_attribute("href")
            print(links)
            # scraper_links = links[30:79]
        # print(scraper_links)


run = ScraperClass(website)
run.cookie_ad_clicker()
# %%
