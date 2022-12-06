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

## Milestone 4
For this milestone I was asked to get data from each corresponding page.

The first task was to create a function to retrieve text and image data from a single details page. I've done this by creating two different methods for extracting text and images. For the image method I done this with the following code below:
```
img_link = driver.find_elements(by=By.XPATH, value='//*[@id="__next"]/div[3]/div/div[2]/div[2]/div[1]/div[1]/div/span/img')
            for img_index in img_link:
                img_link = img_link + [img_index.get_attribute("src")]
            img_link = img_link[1]
```
From the code above you can see that I searched for the specific XPATH element for the image and then pulled the `src` attribute in the `for` loop to get the image url.

For the text method I employed a similar method as shown above:
```
site_text = driver.find_elements(by=By.CLASS_NAME, value="css-srvu6d")
        # print(site_text)
        for text_index in site_text:
            site_text = site_text + [text_index.text]
        site_text = site_text[1]
```
From the code above you can see that I searched for the specific class name instead of the XPATH and used the `.text` function to get the text from the class in the `for` loop.

The next task was to create a dictionary to store all relevant information about the text and image data and to save it locally in a specific folder and name. I created the dictionary by setting it up as a parameter in my class: `        self.dictionary = {"Price Summary": [], "Img Link": [], "Timestamp": [], "ID": []}`. From then it was just a matter of appending the different keys in the dictionary. I saved the dictionary into a specific path and name with the following code below:

```
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

try:    
    open("c:\\Users\\denni\\Desktop\\AiCore\\Projects\\data-collection-pipeline\\raw_data\data.json", "x")
except:
    print("Dictionary file already exists")

```
For the final task i was asked to create a method to use the image links and download the images. I did this using the following code below:
```
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
```
## Milestone 5
For the first task I was asked to refactor and optimise my current code. I have done this by splitting up some of my methods and creating additional methods such as for downloading the image and saving the dictionary locally. The next task was to add docstrings to all of my functions.

The final tasks were to create unit test to test all my public methods in my scraper. I created a separate file to test my methods. I have written my unit tests below:

```
class TestScraperClass(unittest.TestCase):
    def setUp(self):
        self.scraper = scraper_class.ScraperClass

    def test_cookie_ad_clicker(self):
        self.assertEqual(self.scraper.cookie_ad_clicker(self), 1)

    def test_url_link_scraper(self):
        self.assertEqual(self.scraper.url_link_scraper(self), "https://crypto.com/price/bitcoin")
```
From the code above you can see that for my first public method `cookie_ad_clicker()` I am using the `assertEqual` function to check if the method has clicked the reject cookies button by returning the `cookie = 1` variable that is in the `try` statement which would verify that it has clicked the reject cookies button.

For my other public method you can see in `scraper_class.py` under the `url_link_scraper` method that I return the first element of the `links` list. From the code above you can see that I am using the `assertEqual` function again to check that the first element of the list is the link to the bitcoin page. Since the list of the top 50 crypo coins is subject to change I've decided to only check the top coin (Bitcoin) since it is unlikely for it to be removed from the top.

## Milestone 6
For this milestone I was asked to containerise the scraper.

The first task I was asked to do was to run the scraper in headless mode meaning without the GUI. I have done this with the code below:
```
headless = webdriver.FirefoxOptions()
headless.add_argument("--headless")
driver = webdriver.Firefox(options=headless)
```
I had to switch to Firefox since the web scraper was not working properly in Chrome when running headless mode.

The second task was to build and create a Docker image for my scraper. I have done this by creating a Dockerfile:
```
FROM python:3.9

WORKDIR C:\Users\denni\Desktop\AiCore\Projects\data-collection-pipeline
# Update the system and install firefox
RUN apt-get update 
RUN apt -y upgrade 
RUN apt-get install -y firefox-esr

# get the latest release version of firefox 
RUN latest_release=$(curl -sS https://api.github.com/repos/mozilla/geckodriver/releases/latest \
    | grep tag_name | sed -E 's/.*"([^"]+)".*/\1/') && \
    # Download the latest release of geckodriver
    wget https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux32.tar.gz \
    # extract the geckodriver
    && tar -xvzf geckodriver* \
    # add executable permissions to the driver
    && chmod +x geckodriver \
    # Move gecko driver in the system path
    && mv geckodriver C:\Users\denni\Desktop\AiCore\Projects\data-collection-pipeline

COPY scraper_class.py . 
COPY requirements.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "scraper_class.py"]
```
From the Dockerfile above you can see that I've set the working directory and downloaded and installed the latest version of Firefox. I have also had to install the latest version of geckodriver. I have copied the `scraper_class.py` and `requirements.txt` files and installed the latest version of pip and all the packages in the `requirements.txt` file. After the image was created I pushed it to Dockerhub.

## Milestone 7
For this milestone I was asked to set up a CI/CD pipeline for my Docker image.

For the first task I was asked to set up the Github secrets that contain the credentials to log in to my Dockerhub account to be able to push. I created two secrets one which contained my Docker ID as the value and the other my PAT token as the value.

For the last task I was asked to create a Github action that is triggered on a push to the main branch of my repository. I did this by creating a workflow `.yaml` file:
```
name: ci

on:
  push:
    branches:
      - "main"

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      -
        name: Checkout
        uses: actions/checkout@v3
      -
        name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_HUB_USERNAME }}
          password: ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }}
      -
        name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      -
        name: Build and push
        uses: docker/build-push-action@v3
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: ${{ secrets.DOCKER_HUB_USERNAME }}/ci_cd_scraper_img_builder:latest
```
From the code above you can see that the action will be triggered by a push to the main branch. You can also see that I am logging into my Dockerhub account witht he secret variables I created in the previous task which then builds and pushes the image to Dockerhub when a push is made to my Github repository.