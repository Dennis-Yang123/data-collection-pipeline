# %%
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import os
import requests
from uuid import uuid4
from pathlib import Path
from datetime import datetime

headless = webdriver.FirefoxOptions()
headless.add_argument("--headless")
driver = webdriver.Firefox(options=headless)


URL = "https://crypto.com/price"
website = driver.get(URL)

class ScraperClass:

    def __init__(self, website):
        self.website = website
        self.dictionary = {"Price Summary": [], "Img Link": [], "Timestamp": [], "ID": []}
        self.links = []
    
    def cookie_ad_clicker(self):
        """Clicks decline cookie button on webpage

        Uses a delay to allow the cookies option to appear. Then 
        clicks the decline button with the elements XPATH when it 
        appears. It will also run the url_link_scraper method after.
        """

        delay = 10
        try:    
            time.sleep(4)
            driver.execute_script("window.scrollTo(0, 500)")
            time.sleep(2)
            decline_cookies_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-reject-all-handler"]')))
            decline_cookies_button.click()
            cookie = 1

        except TimeoutException:
            print("Loading took too much time.")

        return cookie
    def url_link_scraper(self):
        """Scrapes the links to top 50 current crypto coins

        Finds the links by searching for all a tags in the page.
        Uses a for loop and list slicing to iterate through all
        the relevant elements. Then retrieve all the chosen elements
        and their href attribute. Using list slicing again we can
        get all the links to the top 50 crypto coints.
        """
        driver.execute_script("window.scrollTo(0, 500)")
        self.links= driver.find_elements(by=By.TAG_NAME, value="a")
        
        for link_index in self.links[29:79]:
            self.links = self.links + [link_index.get_attribute("href")]
        self.links = self.links[105:] 
        # print(self.links[0])
        
        time.sleep(2)
        self.__img_scraper()
        self.__text_scraper()
        
        return str(self.links[0])
    
    def __img_scraper(self):
        """Scrapes image from the webpage

        Uses a for loop to go through each wep page in the links 
        list. From the web page we can find the URL for the image
        by using the specific XPATH then using a for loop we can 
        get the src attribute to get the image URL. Then we add to 
        our dictionary by appending the different keys.
        """
        for link_count in self.links:
            time.sleep(1)
            site = driver.get(link_count)
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
            self.dictionary["Timestamp"].append(current_time)
                
            self.__img_downloader(img_link)

            
    def __text_scraper(self):
        """Scrapes text from web page

        Uses a similar for loop to go through the list of links.
        Scrolls down the page to where the text to be scraped is
        located. Then finds the text by searching with the class
        name. Uses a for loop and the .text function to retrieve 
        the text from the page. Updates the dictionary by appending
        the text.
        """
        for link_count in self.links:
            site = driver.get(link_count)
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
        self.__dict_saver()

    def __dict_saver(self):
        """Creates folder for dictionary then saves dictionary locally

        Using the os module we create a path and directory for the
        raw_data folder. We use a try statement to create the folder
        if it already doesn't exist. Then we check if the dictionary 
        file exists and then create it if it does not.
        """
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

        file1 = open("c:\\Users\\denni\\Desktop\\AiCore\\Projects\\data-collection-pipeline\\raw_data\data.json", "w")
        str1 = repr(self.dictionary)
        file1.write("Dictionary = " + str1 + "\n")
        file1.close()

        f = open("c:\\Users\\denni\\Desktop\\AiCore\\Projects\\data-collection-pipeline\\raw_data\data.json", "r")
        if f.mode == "r":
            contents = f.read()
        
        
    def __img_downloader(self, img_link):
        """Downloads the image and saves it locally

        First downloads the image to the incorrect folder then
        moves the file and renames it to the dt_string variable
        to the correct folder
        """
        k = 1
        date_time_now = datetime.now()
        dt_string = date_time_now.strftime("%d%m%Y%H%M%S") + str(k)
        # print(dt_string)
        k += 1
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

  
if __name__ == '__main__':
    run = ScraperClass(website)
    run.cookie_ad_clicker()
    run.url_link_scraper()

# hello    

# %%
