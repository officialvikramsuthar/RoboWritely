import os

from django_cron import CronJobBase, Schedule
from .models import Content
import csv
import openai
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
import time

from handler.chatgpt_selenium_automation import ChatGPTAutomation
import csv
import os


def create_file(filename, content):
    directory_name = "conversations"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    with open(os.path.join(directory_name, file_name), "a") as file:
        file.write(content)



class GenerateContentCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'ContentCreation.GenerateContentCronJob'

    def do(self):

        # Define the path where the chrome driver is installed on your computer
        chrome_driver_path = r"D:\Python\Chatgpt\chromedriver\chromedriver.exe"

        # the sintax r'"..."' is required because the space in "Program Files" 
        # in my chrome_path
        chrome_path = r'"C:\Program Files (x86)\Google\Chrome\Application\Chrome.exe"'

        # Create an instance
        chatgpt = ChatGPTAutomation(chrome_path, chrome_driver_path)

        # opening the CSV file
        with open('keywords.csv', mode ='r')as file:
        
            # reading the CSV file
            csvFile = csv.reader(file)
            
            # displaying the contents of the CSV file
            for index, lines in enumerate(csvFile):
                    if index == 0:
                        continue
                    
                    if len(lines) > 0 and index < 2:
                        print()
                        try:
                            # Define a prompt and send it to chatGPT
                            topic = "".join(lines)
                            prompt = f"""Write an informative and objective article about "{topic}". Your article should provide a comprehensive analysis of the key factors that impact {topic}, including "{topic}". To make your article informative and engaging, be sure to discuss the trade-offs involved in balancing different factors, and explore the challenges associated with different approaches. Your article should also highlight the importance of considering the impact on when making decisions about {topic}. Finally, your article should be written in an informative and objective tone that is accessible to a general audience. Make sure to include the relevant keywords provided by the user, and tailor the article to their interests and needs. Every heading should be in  quotes and square brackets. For example [{topic} Heading ] and title should be in <> for example  <{topic}>"""
                            chatgpt.send_prompt_to_chatgpt(prompt)

                            # Retrieve the last response from chatGPT
                            response = chatgpt.return_last_response()
                            
                            file_name = "{}.txt".format(topic)
                            create_file(file_name, response)

                        except Exception as e:
                            print(e)
                            chatgpt.star_new_chat()

            chatgpt.quit()