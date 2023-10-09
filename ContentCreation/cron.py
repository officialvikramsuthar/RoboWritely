


from django_cron import CronJobBase, Schedule
from selenium.webdriver.support.wait import WebDriverWait

from ContentCreation.handler.ChromeDriverSetup import ChromeDriverAutomation
from ContentCreation.handler.chatgpt_selenium_automation import ChatGPTAutomation
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
import platform
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from ContentCreation.models import BlogPost, Paragraph
from ContentCreation.utils import CreateGptBlog, AudioBookPrompts, move_files
from selenium import webdriver
import os
import requests
from PIL import Image
from io import BytesIO
import time


def create_file(filename, content, directory_name="conversations"):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    with open(os.path.join(directory_name, filename), "a") as file:
        file.write(content)


class GenerateContentCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'ContentCreation.GenerateContentCronJob'

    def do(self):

        get_platform = platform.platform()
        if "Linux" in get_platform:
            BASE_DIR = os.path.dirname(os.path.realpath(__file__))
            chrome_driver_path = os.path.join(BASE_DIR, "../../chromedriver/chromedriver")
            chrome_path = r'"/opt/google/chrome/chrome"'
            # Create an instance
            chatgpt = ChatGPTAutomation(chrome_path, chrome_driver_path)
            file_path = os.path.join(BASE_DIR, "keywords.csv")

        else:
            # Define the path where the chrome driver is installed on your computer
            chrome_driver_path = r"D:\Python\RoboWritely\ContentCreation\chromedriver\chromedriver.exe"

            # the sintax r'"..."' is required because the space in "Program Files"
            # in my chrome_path
            chrome_path = r'"C:\Program Files (x86)\Google\Chrome\Application\Chrome.exe"'
            # Create an instance
            chatgpt = ChatGPTAutomation(chrome_path, chrome_driver_path)
            file_path = 'D:\Python\RoboWritely\ContentCreation\keywords.csv'

        # opening the CSV file
        with open(file_path, mode='r') as file:

            # reading the CSV file
            csvFile = csv.reader(file)

            # displaying the contents of the CSV file
            for index, lines in enumerate(csvFile):
                if index == 0:
                    continue

                if len(lines) > 0:

                    try:
                        chatgpt.star_new_chat()
                        topic = "".join(lines)
                        obj = CreateGptBlog(topic)
                        blog = []

                        # Meta Description
                        meta_description_prompt = obj.get_title_prompt()
                        chatgpt.send_prompt_to_chatgpt(meta_description_prompt)
                        meta_description_response = chatgpt.return_last_response()
                        blog.append("<meta>" + meta_description_response + "</meta>")

                        # Title
                        title_prompt = obj.get_title_prompt()
                        chatgpt.send_prompt_to_chatgpt(title_prompt)
                        title_response = chatgpt.return_last_response()
                        blog.append("<title>" + title_response + "</title>")
                        blog.append("<h1>"+title_response+"</h1>")

                        # Headings and set headings
                        headings_prompt = obj.get_heading_prompt()
                        chatgpt.send_prompt_to_chatgpt(headings_prompt)
                        heading_response = chatgpt.return_last_response()
                        obj.set_heading(heading_response)

                        # Intro
                        blog.append("<div class='blog-intro'>")
                        intro_prompt = obj.get_intro_prompt()
                        chatgpt.send_prompt_to_chatgpt(intro_prompt)
                        intro_response = chatgpt.return_last_response()
                        blog.append("<h2>Introduction</h2>")
                        blog.append("<p class='blog-intro'>"+intro_response+"</p>")
                        blog.append("</div>")

                        # Loop Through all Headings
                        for heading in obj.heading_list:
                            blog.append("<div class='blog-subsection'>")
                            blog.append("<h2 class='blog-sub-heading'>"+heading.strip('"')+"</h2>")
                            heading_prompt_para = obj.get_heading_para_prompt(heading)
                            chatgpt.send_prompt_to_chatgpt(heading_prompt_para)
                            heading_prompt_response = chatgpt.return_last_response()
                            heading_prompt_response = heading_prompt_response.replace(heading, "")
                            blog.append("<p class='blog-sub-heading-para'>"+heading_prompt_response+"</p>")
                            blog.append("</div>")


                        # Adding Conclusion
                        blog.append("<div class='blog-conclusion'>")
                        conlusion_prompt = obj.get_conclusion_prompt()
                        chatgpt.send_prompt_to_chatgpt(conlusion_prompt)
                        conlusion_response = chatgpt.return_last_response()
                        blog.append("<h2>Conclusion</h2>")
                        blog.append("<p class='conclusion-para'>"+conlusion_response+"</p>")
                        blog.append("</div>")

                        response = "".join(blog)
                        file_name = "{}.txt".format(topic)
                        create_file(file_name, response)

                    except Exception as e:
                        print(e)
                        chatgpt.star_new_chat()

            chatgpt.quit()


class StoreContentFromFile(CronJobBase):

    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'ContentCreation.StoreContentFromFile'


    def do(self):
        get_platform = platform.platform()
        folder_path = ""

        if "Linux" in get_platform:
            BASE_DIR = os.path.dirname(os.path.realpath(__file__))
            folder_path = os.path.join(BASE_DIR, "../conversations/")

        else:
            pass

        # Check if the folder exists
        if os.path.exists(folder_path):
            # Loop through all the files in the folder
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)

                # Check if it's a file (not a subdirectory)
                if os.path.isfile(file_path):
                    with open(file_path, 'r') as f:
                        blog = BlogPost()
                        test = f.read()
                        soup = BeautifulSoup(test, 'html.parser')
                        title = ""
                        paragraphs = test

                        for title_tag in soup.find_all('title'):
                            title = str(title_tag.extract())
                            paragraphs = paragraphs.replace(title, "")
                            blog.title = title

                        for meta_tag in soup.find_all('meta'):
                            meta = str(meta_tag.extract())
                            paragraphs = paragraphs.replace(meta, "")
                            blog.meta = meta

                        divs_with_class = soup.find_all('div', class_='blog-intro')
                        intro_content = ""

                        for intro in divs_with_class:
                            intro = str(intro)
                            intro_content = intro
                            intro = intro.replace("<h2>Introduction</h2>", "")
                            blog.intro = intro

                        keywords = title.replace("<title>", "")
                        keywords = keywords.replace("</title>", "")
                        blog.heading = keywords
                        blog.keyword = keywords
                        blog.slug = keywords
                        blog.save()

                        blog_content = Paragraph()
                        blog_content.blog_post = blog
                        blog_content.content = intro
                        blog_content.save()

                        divs_with_class = soup.find_all('div', class_='blog-subsection')
                        for div in divs_with_class:
                            blog_content = Paragraph()
                            blog_content.blog_post = blog
                            blog_content.content = str(div)
                            blog_content.save()

                        divs_with_class = soup.find_all('div', class_='blog-conclusion')

                        for conslusion in divs_with_class:
                            conslusion = str(conslusion)
                            blog_content = Paragraph()
                            blog_content.blog_post = blog
                            blog_content.content = conslusion
                            blog_content.save()

        else:
            print(f"The folder '{folder_path}' does not exist.")

class get_products_from_amazon(CronJobBase):

    def do(self):
        get_platform = platform.platform()
        if "Linux" in get_platform:
            BASE_DIR = os.path.dirname(os.path.realpath(__file__))
            chrome_driver_path = os.path.join(BASE_DIR, "../../chromedriver/chromedriver")
            chrome_path = r'"/opt/google/chrome/chrome"'
            # Create an instance
            amazon = ChromeDriverAutomation(chrome_path, chrome_driver_path, "https://www.amazon.com")
            file_path = os.path.join(BASE_DIR, "keywords.csv")

        else:
            pass

        # Set up Selenium WebDriver (make sure you have the appropriate WebDriver installed)
        driver = amazon.driver  # Replace with your path
        time.sleep(10)
        # Define a list of price ranges
        price_ranges = [
            ("0-25", "25"),
            ("25-50", "50"),
            ("50-100", "100"),
            ("100-200", "200"),
            ("200-500", "500")
        ]

        # Initialize a dictionary to store product details
        product_details = {}

        # Iterate through each price range
        for price_range in price_ranges:
            search_box = driver.find_element(By.ID, "twotabsearchtextbox")
            search_box.clear()
            search_box.send_keys(f"Books under ${price_range[1]}")
            search_box.send_keys(Keys.RETURN)
            time.sleep(10)
            # Sort by Highest to Lowest Customer Review
            driver.find_element(By.XPATH, '//*[@id="s-result-sort-select_3"]').click()
            time.sleep(5)  # Allow the page to load

            # Find and store product details
            product_elements = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")

            for index, product_element in enumerate(product_elements[:10], start=1):
                product_title = product_element.find_element(By.XPATH, ".//span[@class='a-text-normal']").text
                product_price = product_element.find_element(By.XPATH, ".//span[@class='a-offscreen']").text
                product_url = product_element.find_element(By.XPATH, ".//a[@class='a-link-normal']").get_attribute(
                    "href")

                product_details[f"Product {index}"] = {
                    "Title": product_title,
                    "Price": product_price,
                    "URL": product_url
                }

            # Go back to the search results page
            driver.execute_script("window.history.go(-1)")
            time.sleep(2)  # Allow the page to load

        # Print the scraped data
        for key, value in product_details.items():
            print(f"{key}:")
            print(f"Title: {value['Title']}")
            print(f"Price: {value['Price']}")
            print(f"URL: {value['URL']}")
            print("=" * 40)

        # Close the WebDriver
        amazon.quit()


class LinkedinScraperFromGoolge(CronJobBase):

    def do(self):

        # Define the search string and the number of images to scrape
        search_string = "The NBA's Elite: Top 10 All-Time Scorers"
        num_images_to_scrape = 10  # You can change this as needed

        get_platform = platform.platform()
        if "Linux" in get_platform:
            BASE_DIR = os.path.dirname(os.path.realpath(__file__))
            chrome_driver_path = os.path.join(BASE_DIR, "../../chromedriver/chromedriver")
            chrome_path = r'"/opt/google/chrome/chrome"'
            # Create an instance
            amazon = ChromeDriverAutomation(chrome_path, chrome_driver_path, "https://www.linkedin.com/in/warikoo/recent-activity/all/")
            file_path = os.path.join(BASE_DIR, "keywords.csv")

        else:
            pass

        # Set up Selenium WebDriver (make sure you have the appropriate WebDriver installed)
        driver = amazon.driver
        time.sleep(10)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)


        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)


        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)


        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)


        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)


        post = driver.find_elements(By.CSS_SELECTOR, "div.update-components-update-v2__commentary")

        for element in post:
            inner_text = element.text
            content = "\n\n New Post By Ankoor\n" + inner_text
            create_file("ankoor_warikoo.txt",content)

        driver.close()


class TrendlyneAPI(CronJobBase):

    def do(self):

        # Define the search string and the number of images to scrape
        search_string = "The NBA's Elite: Top 10 All-Time Scorers"
        num_images_to_scrape = 10  # You can change this as needed

        get_platform = platform.platform()
        if "Linux" in get_platform:
            BASE_DIR = os.path.dirname(os.path.realpath(__file__))
            chrome_driver_path = os.path.join(BASE_DIR, "../../chromedriver/chromedriver")
            chrome_path = r'"/opt/google/chrome/chrome"'
            # Create an instance
            amazon = ChromeDriverAutomation(chrome_path, chrome_driver_path, "https://trendlyne.com/clientapi/irwin/webview/FHZVJwFXDC/portfolio-report/")
            file_path = os.path.join(BASE_DIR, "keywords.csv")

        else:
            pass

        # Set up Selenium WebDriver (make sure you have the appropriate WebDriver installed)
        driver = amazon.driver
        time.sleep(10)
        window_scrip = '''const payload = JSON.stringify({
              source: "trendlyne",
              data: {
        "holdings": [
          {
            "qty": 12,
            "avgPrice": 600.92,
            "ISIN": "INF789FB1X58",
            "stockCode": "",
            "LTP": 723.12
          },
          {
            "qty": 500,
            "avgPrice": 80.92,
            "ISIN": "INF200K01UG1",
            "stockCode": "",
            "LTP": 93.29
          },
          {
            "qty": 500,
            "avgPrice": 26.02,
            "ISIN": "INF663L01FF1",
            "stockCode": "",
            "LTP": 31.8
          },
          {
            "qty": 200,
            "avgPrice": 20.32,
            "ISIN": "INF174K01JI7",
            "stockCode": "",
            "LTP": 45.86
          },
          {
            "qty": 10,
            "avgPrice": 2500.46,
            "ISIN": "INF200K01MO2",
            "stockCode": "",
            "LTP": 2873.43
          },
          {
            "qty": 14,
            "avgPrice": 400.24,
            "ISIN": "INF109K01O82",
            "stockCode": "",
            "LTP": 476.18
          },
          {
            "qty": 5,
            "avgPrice": 250.24,
            "ISIN": "INF109K01O82",
            "stockCode": "",
            "LTP": 249.18
          },
          {
            "qty": 30,
            "avgPrice": 200.5,
            "ISIN": "INF200K01107",
            "stockCode": "",
            "LTP": 222.69
          },
          {
            "qty": 15,
            "avgPrice": 350.42,
            "ISIN": "INF209K01KE8",
            "stockCode": "",
            "LTP": 404.03
          },
          {
            "qty": 15,
            "avgPrice": 45.17,
            "ISIN": "INF879O01027",
            "stockCode": "",
            "LTP": 61.07
          },
          {
            "qty": 12,
            "avgPrice": 350.1,
            "stockCode": "AUROPHARMA",
            "ISIN": "",
            "LTP": 700
          },
          {
            "qty": 300,
            "avgPrice": 19.1,
            "stockCode": "MAHABANK",
            "ISIN": "",
            "LTP": 36.15
          },
          {
            "qty": 20,
            "avgPrice": 230.0,
            "stockCode": "COALINDIA",
            "ISIN": "",
            "LTP": 229.25
          },
          {
            "qty": 10,
            "avgPrice": 230.0,
            "stockCode": "COALINDIA",
            "ISIN": "",
            "LTP": 229.25
          },
          {
            "qty": 200,
            "avgPrice": 30.6,
            "stockCode": "SPICEJET",
            "ISIN": "",
            "LTP": 29.87
          },
          {
            "qty": 100,
            "avgPrice": 90,
            "stockCode": "ASIANHOTNR",
            "ISIN": "",
            "LTP": 155
          },
          {
            "qty": 20,
            "avgPrice": 300,
            "stockCode": "505681",
            "ISIN": "",
            "LTP": 515
          },
          {
            "qty": 40,
            "avgPrice": 35,
            "stockCode": "SJVN",
            "ISIN": "",
            "LTP": 55.85
          },
          {
            "qty": 10,
            "avgPrice": 1250,
            "stockCode": "INDUSINDBK",
            "ISIN": "",
            "LTP": 1403
          },
          {
            "qty": 12,
            "avgPrice": 800,
            "stockCode": "BDL",
            "ISIN": "",
            "LTP": 1115.05
          },
          {
            "qty": 3,
            "avgPrice": 2500,
            "stockCode": "POLYCAB",
            "ISIN": "",
            "LTP": 4660.2
          }
        ]
      },
            });
window.postMessage(payload, "*");
'''
        driver.execute_script(window_scrip)
        time.sleep(10)

        driver.close()


class GetAudiobookConversations(CronJobBase):

    def do(self):
        get_platform = platform.platform()
        if "Linux" in get_platform:
            BASE_DIR = os.path.dirname(os.path.realpath(__file__))
            chrome_driver_path = os.path.join(BASE_DIR, "../../chromedriver/chromedriver")
            chrome_path = r'"/opt/google/chrome/chrome"'
            # Create an instance
            chatgpt = ChatGPTAutomation(chrome_path, chrome_driver_path)
            file_path = os.path.join(BASE_DIR, "audio_books.csv")

        else:
            pass

        with open(file_path, mode='r') as file:
            # reading the CSV file
            csvFile = csv.reader(file)
            # displaying the contents of the CSV file
            chatgpt.star_new_chat()

            for index, lines in enumerate(csvFile):
                if index == 0:
                    continue

                if len(lines) > 0 and index < 10:
                    try:
                        audio_obj = AudioBookPrompts()
                        topic = "".join(lines)
                        audio_prompt = audio_obj.get_audio_book_prompt(topic)
                        chatgpt.send_prompt_to_chatgpt(audio_prompt)
                        time.sleep(30)
                        response = chatgpt.return_last_response()
                        file_name = "{}.txt".format(topic)
                        create_file(file_name, response, directory_name="audiobooks")

                    except Exception as e:
                        print(e)
                        chatgpt.star_new_chat()


class ConvertAudioBooks(CronJobBase):

    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'ContentCreation.StoreContentFromFile'


    def do(self):
        get_platform = platform.platform()
        folder_path = ""

        if "Linux" in get_platform:
            BASE_DIR = os.path.dirname(os.path.realpath(__file__))
            folder_path = os.path.join(BASE_DIR, "../audiobooks/")

        else:
            pass

        get_platform = platform.platform()
        if "Linux" in get_platform:
            BASE_DIR = os.path.dirname(os.path.realpath(__file__))
            chrome_driver_path = os.path.join(BASE_DIR, "../../chromedriver/chromedriver")
            chrome_path = r'"/opt/google/chrome/chrome"'
            # Create an instance
            elevenlabs = ChromeDriverAutomation(chrome_path, chrome_driver_path, "https://elevenlabs.io/", download_folder=folder_path)

        else:
            pass

        # Set up Selenium WebDriver (make sure you have the appropriate WebDriver installed)
        driver = elevenlabs.driver
        time.sleep(10)
        button_script = """var xpath = "//button[text()='Daniel']";var matchingElement = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;matchingElement.click()"""
        dropdown = driver.execute_script(button_script)

        select_script = """var xpath = "//li[text()='Mimi']";var matchingElementLi = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;matchingElementLi.click()"""
        dropdown = driver.execute_script(button_script)

        # Check if the folder exists
        if os.path.exists(folder_path):
            # Loop through all the files in the folder
            for index, filename in enumerate(os.listdir(folder_path)):
                file_path = os.path.join(folder_path, filename)

                if index != 1:
                    pass

                BASE_DIR = BASE_DIR = os.path.dirname(os.path.realpath(__file__))
                CurrentDownloadDir = os.path.join(BASE_DIR, "../../../../download_audios")
                NewDownloadDir = os.path.join(CurrentDownloadDir, "../../../../download_audios/" + filename)
                # Check if it's a file (not a subdirectory)
                if os.path.isfile(file_path):
                    with open(file_path, 'r') as f:
                        file_content = f.read()

                        audio_book_list = file_content.split('\n')

                        for a in audio_book_list:
                            input_box = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[data-testid='tryout-textarea']")))
                            input_box.clear()
                            input_box.send_keys(a)
                            time.sleep(2)
                            play_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, 'button[aria-label="Play"]')))
                            play_button.click()
                            time.sleep(40)
                            download = driver.find_element(By.CSS_SELECTOR, value='svg > path[d="M10.75 2.75a.75.75 0 00-1.5 0v8.614L6.295 8.235a.75.75 0 10-1.09 1.03l4.25 4.5a.75.75 0 001.09 0l4.25-4.5a.75.75 0 00-1.09-1.03l-2.955 3.129V2.75z"]')
                            download.click()
                            time.sleep(2)


                        move_files(CurrentDownloadDir, NewDownloadDir)





def get_data_from_google_maps():
    get_platform = platform.platform()
    if "Linux" in get_platform:
        BASE_DIR = os.path.dirname(os.path.realpath(__file__))
        chrome_driver_path = os.path.join(BASE_DIR, "../../chromedriver/chromedriver")
        chrome_path = r'"/opt/google/chrome/chrome"'
        # Create an instance
        maps = ChromeDriverAutomation(chrome_path, chrome_driver_path,
                                        "https://www.google.com/maps/search/dermatologist+melbourne/@-37.8526081,145.0112638,12z/data=!4m2!2m1!6e1?entry=ttu")
        file_path = os.path.join(BASE_DIR, "keywords.csv")

    else:
        pass

    # Set up Selenium WebDriver (make sure you have the appropriate WebDriver installed)
    driver = maps.driver
    time.sleep(5)
    Y = 300
    X = 100
    driver.execute_script(f'document.querySelector("#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd").scrollTo({X}, {Y})')

    for i in range(0, 5):
        time.sleep(2)
        Y = Y * 2

    getLinks = driver.find_elements(By.CSS_SELECTOR, 'a.hfpxzc')

    all_links = []
    for i in getLinks:
        all_links.append(i.get_attribute('href'))

    all_details = []
    for i in all_links:
        driver.get(i)
        time.sleep(3)
        name = driver.find_element(By.CSS_SELECTOR, "h1.DUwDvf").text
        all_info = driver.find_elements(By.CSS_SELECTOR, "div.Io6YTe")
        phone = ""
        address = ""
        if len(all_info) > 4:
            address = all_info[0].text
            phone = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[6]/button/div/div[2]/div[1]').text

        elif len(all_info) >= 1:
            address = all_info[0].text

        details = [name, address, phone]

        all_details.append(details)

    # Specify the file name for the CSV file
    file_name = "map_all_data.csv"

    # Open the CSV file in write mode
    with open(file_name, mode='w', newline='') as file:
        # Create a CSV writer object
        writer = csv.writer(file)

        # Write the data to the CSV file row by row
        for row in all_details:
            writer.writerow(row)


















