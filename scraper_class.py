# %%
from selenium import webdriver 
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
URL = "https://www.xe.com/currencyconverter/convert/?Amount=1&From=GBP&To=USD"
website = driver.get(URL)


class ScraperClass:
    def __init__(self, website):
        self.website = website

    def cookie_ad_clicker(self):
        time_now  = time.time()
        try:    
            accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@class="button__BaseButton-sc-1qpsalo-0 haqezJ"]')
            accept_cookies_button.click()
            while time.time() < time_now + 5:
                decline_ad = driver.find_element(by=By.XPATH, value='//*[@id="element-0JgZU8"]') 
                decline_ad.click()
        except AttributeError:
            accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="button__BaseButton-sc-1qpsalo-0 haqezJ"]')
            accept_cookies_button.click()
            while time.time() < time_now + 5:
                decline_ad = driver.find_element(by=By.XPATH, value='//*[@id="element-0JgZU8"]') 
                decline_ad.click()

        except:
            pass

run = ScraperClass(website)
run.cookie_ad_clicker()
# %%
