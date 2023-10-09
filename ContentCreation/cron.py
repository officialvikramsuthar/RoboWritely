


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


















