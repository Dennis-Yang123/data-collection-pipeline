# %%
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import os
import requests
from uuid import uuid4
from pathlib import Path
from datetime import datetime

driver = webdriver.Chrome()
URL = "https://crypto.com/price"
website = driver.get(URL)


class ScraperClass:
    def __init__(self, website):
        self.website = website
        self.dictionary = {"Price Summary": [], "Img Link": [], "Timestamp": [], "ID": []}
    
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
        self.img_scraper(links)
        self.text_scraper(links)
        


    def img_scraper(self, links):
            k = 1
            time.sleep(1)
            data_url = links[0]
            site = driver.get(data_url)
            id = str(uuid4())
            time.sleep(2)
            img_link = driver.find_elements(by=By.XPATH, value='//*[@id="__next"]/div[3]/div/div[2]/div[2]/div[1]/div[1]/div/span/img')
            for img_index in img_link:
                img_link = img_link + [img_index.get_attribute("src")]
            img_link = img_link[1]
            # print(img_link)
            self.dictionary["Img Link"].append(img_link)
            self.dictionary["ID"].append(id)
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            date_time_now = datetime.now()
            dt_string = date_time_now.strftime("%d%m%Y%H%M%S") + str(k)
            print(dt_string)
            k += 1
            self.dictionary["Timestamp"].append(current_time)

            try:
                img_data = requests.get(img_link).content
                with open("test_image.png", "wb") as handler:
                    handler.write(img_data)
            except:
                print("Image file already exists")
            
            try:
                Path(r"c:\\Users\\denni\\Desktop\\AiCore\\Projects\\data-collection-pipeline\test_image.png").rename(f"c:\\Users\\denni\\Desktop\\AiCore\\Projects\\data-collection-pipeline\\raw_data\\images\{dt_string}.png")
            except:
                print("Image file already exists")


    def text_scraper(self, links):

        # for x in links:
        data_url = links[0]
        site = driver.get(data_url)
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 1350)")
        time.sleep(2)

        site_text = driver.find_elements(by=By.CLASS_NAME, value="css-srvu6d")
        # print(site_text)
        for text_index in site_text:
            site_text = site_text + [text_index.text]
        site_text = site_text[1]
        # print(site_text) # Prints crypto price summaries
        self.dictionary["Price Summary"].append(site_text)
        
        print(self.dictionary)

directory = "raw_data"
parent_directory = "c:\\Users\\denni\\Desktop\\AiCore\\Projects\\data-collection-pipeline"
path = os.path.join(parent_directory, directory) 

try:
    os.mkdir(path)
except OSError as error:
    print("Folder already exists")



try:    
    open("c:\\Users\\denni\\Desktop\\AiCore\\Projects\\data-collection-pipeline\\raw_data\data.json", "x")
except:
    print("Dictionary file already exists")


if __name__ == '__main__':
    run = ScraperClass(website)
    run.cookie_ad_clicker()

dict_file = open("c:\\Users\\denni\\Desktop\\AiCore\\Projects\\data-collection-pipeline\\raw_data\data.json", "w")
str_dict = repr(run.dictionary)
dict_file.write("Dictionary = " + str_dict + "\n")

f = open("c:\\Users\\denni\\Desktop\\AiCore\\Projects\\data-collection-pipeline\\raw_data\data.json", "r")
if f.mode == "r":
    contents = f.read()

# %%
