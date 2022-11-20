# Data Collection Pipeline
## Milestone 3
For this milestone I was asked to build an initial scraper class and the website I have chosen in https://crypto.com/price to try and scrape data from the Top 50 current crypto coins.

To build the scraper class I used the selenium to build my webscraper. One of the first tasks was to bypass cookies which I have done by:
```
decline_cookies_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-reject-all-handler"]')))

decline_cookies_button.click()
```
From the code above you can see I have implemented a delay of 10 seconds before it tries to detect the decline button element due to variations in loading time for the website. After it detects the presence of the button we can identify it via its XPATH and id and use the click method to click the button and decline the cookies.

One of the other tasks was to create a method to get links to each page where details can be found and store it in a list. I have done this by:
```
def url_link_scraper(self):
        links = []
        links = links + driver.find_elements(by=By.TAG_NAME, value="a")
        
        for index in links[29:79]:
            links = index.get_attribute("href")
            print(links)
            
        return(links)
```
From the code above you can see that I create a `links` variable which is initially an empty list and then we add to the empty list using the `driver.find_elements()` function to identify all the `a` tags in the webpage. Using a `for` loop and list indexing we can select all the relevant `a` tags relating to the top 50 crypto coins. Looking inside the `for` loop we overwrite the links variable by iterating through the previous `links` variable and printing the `href` attribute which would have the links to all the top 50 crypto coins.