


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
from icecream import ic


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


class ScrapAmazonData(CronJobBase):

    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'ContentCreation.ScrapAmazonData'


    def do(self):

        # for pageNo in range(1, 3):
        pageNo =1
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
                   "Connection": "close", "Upgrade-Insecure-Requests": "1"}

        r = requests.get(
            'https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_' + str(pageNo) + '?ie=UTF8&pg=' + str(pageNo),
            headers=headers)  # , proxies=proxies)
        content = r.content
        soup = BeautifulSoup(content)

        alls = []
        for d in soup.findAll('div', attrs={'class': '_cDEzb_grid-column_2hIsc'}):
            # print(d)
            name = d.find('div', attrs={'class':'p13n-sc-uncoverable-faceout'})
            n = name.find_all('img', alt=True)
            # print(n[0]['alt'])
            author = d.find('a', attrs={'class': 'a-size-small a-link-child'})
            ratings_div = d.find('div', attrs={'class':'a-icon-row'})
            rating = None
            users_rated = None
            if ratings_div:
                rating = ratings_div.find('span', attrs={'class': 'a-icon-alt'})
                users_rated = ratings_div.find('span', attrs={'class': 'a-size-small'})

            price = d.find('span', attrs={'class': 'a-size-base a-color-price'})
            link = d.find('a', attrs={'class':'a-link-normal'})
            # import ipdb;ipdb.set_trace()

            all1 = []

            if name is not None:
                # print(n[0]['alt'])
                all1.append(n[0]['alt'])
            else:
                all1.append("unknown-product")

            if author is not None:
                # print(author.text)
                all1.append(author.text)

            elif author is None:
                author = d.find('div', attrs={'class': 'a-size-small a-color-base'})
                if author is not None:
                    all1.append(author.text)
                else:
                    all1.append('0')

            if rating is not None:
                # print(rating.text)
                all1.append(rating.text)
            else:
                all1.append('-1')

            if users_rated is not None:
                # print(price.text)
                ic(users_rated.text)
                all1.append(users_rated.text)
            else:
                all1.append('0')

            if price is not None:
                # print(price.text)
                all1.append(price.text)
            else:
                all1.append('0')

            if link :
                all1.append(link.attrs.get('href'))
            else:
                all1.append(link)

            alls.append(all1)

        ic(alls)

        file_name = "amazon_data.csv"
        with open(file_name, mode='w', newline='') as file:
            # Create a CSV writer object
            writer = csv.writer(file)

            # Write the data to the CSV file row by row
            for row in alls:
                writer.writerow(row)

        return alls


# For amazon.com
class ScrapAmazonComData(CronJobBase):

    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'ContentCreation.ScrapAmazonData'


    def do(self):

        get_platform = platform.platform()
        if "Linux" in get_platform:
            BASE_DIR = os.path.dirname(os.path.realpath(__file__))
            chrome_driver_path = os.path.join(BASE_DIR, "../../chromedriver/chromedriver")
            chrome_path = r'"/opt/google/chrome/chrome"'
            # Create an instance
            amazon = ChromeDriverAutomation(chrome_path, chrome_driver_path, "https://www.amazon.com/s?k=polaroid+camera&i=electronics-intl-ship&rh=p_72%3A2661618011&dc&ds=v1%3APfZ9V3Llthdu8z9LVGfLkxOspkgQ1Hm3dfImt68bgXg&crid=1LV8RDQWQSIYF&qid=1697190841&rnid=2661617011&sprefix=polariod+camer%2Celectronics-intl-ship%2C321&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&ref=sr_nr_p_72_1")
            file_path = os.path.join(BASE_DIR, "keywords.csv")

        else:
            pass

        # Set up Selenium WebDriver (make sure you have the appropriate WebDriver installed)
        driver = amazon.driver
        time.sleep(5)
        for i in range(0, 2):
            driver.execute_script("window.scrollTo({}, document.body.scrollHeight);".format(i * 100))
            time.sleep(2)

        content = driver.page_source
        # ic(content)
        soup = BeautifulSoup(content)

        alls = []
        ic(len(soup.findAll('div', attrs={'class': ['puis-card-container',
                                                             's-card-container',
                                                             's-overflow-hidden',
                                                             'aok-relative',
                                                             'puis-include-content-margin',
                                                             'puis',
                                                             'puis-v3vtwxgppca0z12v18v51zrqona',
                                                             's-latency-cf-section',
                                                             's-card-border']
                                                            })))
        for d in soup.findAll('div', attrs={'class': ['puis-card-container',
                                                             's-card-container',
                                                             's-overflow-hidden',
                                                             'aok-relative',
                                                             'puis-include-content-margin',
                                                             'puis',
                                                             'puis-v3vtwxgppca0z12v18v51zrqona',
                                                             's-latency-cf-section',
                                                             's-card-border']
                                                            }):
            # print(d)
            name = d.find('h2')
            n = d.find_all('img', alt=True)

            ratings_div = d.find('div', attrs={'class':'a-section a-spacing-none a-spacing-top-micro'})
            rating = None
            users_rated = None
            price_div = d.find('span', attrs={'class':'a-price'})


            if ratings_div:
                rating = ratings_div.find('span', attrs={'class': 'a-icon-alt'})
                users_rated = ratings_div.find('span', attrs={'class': 'a-size-base s-underline-text'})

            price = None

            if price_div:
                price = price_div.find('a-offscreen', attrs={'class':'a-offscreen'})

            link = d.find('a', attrs={'class':'a-link-normal'})
            # import ipdb;ipdb.set_trace()

            all1 = []

            if not name and not rating and not link:
                continue

            if name is not None:
                # print(n[0]['alt'])
                all1.append(n[0]['alt'])
            else:
                all1.append("unknown-product")

            if rating is not None:
                # print(rating.text)
                all1.append(rating.text)
            else:
                all1.append('-1')

            if users_rated is not None:
                # print(price.text)
                ic(users_rated.text)
                all1.append(users_rated.text)
            else:
                all1.append('0')

            if price is not None:
                # print(price.text)
                all1.append(price.text)
            else:
                all1.append('0')

            if link :
                all1.append(link.attrs.get('href'))
            else:
                all1.append(link)

            alls.append(all1)

        ic(alls)

        file_name = "amazon_data_product.csv"
        with open(file_name, mode='w', newline='') as file:
            # Create a CSV writer object
            writer = csv.writer(file)

            # Write the data to the CSV file row by row
            for row in alls:
                writer.writerow(row)

        driver.quit()

        return alls



class ScrapAmazonProductData(CronJobBase):

    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'ContentCreation.ScrapAmazonProductData'


    def do(self):

        get_platform = platform.platform()
        if "Linux" in get_platform:
            BASE_DIR = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(BASE_DIR, "../amazon_data_product.csv")

        base_url = "https://www.amazon.com"
        with open(file_path, mode='r') as file:
            csvFile = csv.reader(file)

            all_info = []

            for row in csvFile:
                if row[0] == "unknown-product" or "Sponsred Ad" in row[0] :
                    ic("skipping")
                    continue

                time.sleep(3)
                product_url = base_url + row[4]

                try:
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
                        "Connection": "close", "Upgrade-Insecure-Requests": "1"}

                    r = requests.get(product_url,
                                     headers=headers)  # , proxies=proxies)
                    content = r.content
                    soup = BeautifulSoup(content)

                    all1 = []
                    about_device_div = soup.find("div", attrs={"id": "feature-bullets"})

                    if about_device_div:
                        all1.append(about_device_div.text)
                    else:
                        all1.append("No Description Found")

                    price_div = soup.find("span", attrs={"class": "priceToPay"})

                    if price_div:
                        price = price_div.find("span", attrs={"class": "a-offscreen"})

                        if price:
                            all1.append(price.text)

                        else:
                            all1.append("Price Could not found")

                    else:
                        all1.append("Price Could not")

                    details = soup.find("table", attrs={"class":"prodDetTable"})

                    if details:
                        all1.append(details.text)

                    else:
                        all1.append("Could not find details")


                    all_info.append(all1)

                except Exception as e:
                    print(e)

            file_name = "product_details.csv"
            with open(file_name, mode='w', newline='') as file:
                # Create a CSV writer object
                writer = csv.writer(file)

                # Write the data to the CSV file row by row
                for row in all_info:
                    writer.writerow(row)















