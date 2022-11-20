# %%
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time


driver = webdriver.Chrome()
URL = "https://crypto.com/price"
website = driver.get(URL)


class ScraperClass:
    def __init__(self, website):
        self.website = website

    def cookie_ad_clicker(self):
        delay = 10
        try:    
            time.sleep(4)
            driver.execute_script("window.scrollTo(0, 500)")
            time.sleep(2)
            decline_cookies_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-reject-all-handler"]')))
            decline_cookies_button.click()
            self.url_link_scraper()

        except TimeoutException:
            print("Loading took too much time.")


    def url_link_scraper(self):
        links= driver.find_elements(by=By.TAG_NAME, value="a")
        
        for index in links[29:79]:
            links = links + [index.get_attribute("href")]
        links = links[105:] 
        # print(links)
        
        time.sleep(2)
        self.text_scraper(links)
        self.img_scraper(links)


    def text_scraper(self, links):

        # for x in links:
        data_url = links[0]
        site = driver.get(data_url)
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 1350)")
        time.sleep(2)

        site_text = driver.find_elements(by=By.TAG_NAME, value="p")
        # print(site_text)
        for text_index in site_text:
            site_text = site_text + [text_index.text]
        site_text = site_text[332]
        print(site_text) # Prints crypto price summaries
        

    def img_scraper(self, links):
        data_url = links[0]
        site = driver.get(data_url)
        time.sleep(2)
        img_link = driver.find_elements(by=By.TAG_NAME, value="img")
        for img_index in img_link:
            img_link = img_link + [img_index.get_attribute("src")]
        
        img_link = img_link[158]
        print(img_link)




if __name__ == '__main__':
    run = ScraperClass(website)
    run.cookie_ad_clicker()
    
# %%
