
from django_cron import CronJobBase, Schedule
from .models import Content
import csv
import openai
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from .utils import generate_content_with_keywords


class GenerateContentCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'contentgenerator.generate_content_cron_job'

    def do(self):
        # Set up your OpenAI API key
        file_path =
        with open('.csv', 'r') as csv_file:
                            
                # Path to your WebDriver executable (e.g., chromedriver.exe)
                driver_path = '/path/to/your/webdriver'

                # URL of the website you want to visit (e.g., ChatGPT interface)
                website_url = 'https://www.example.com'

                # Text you want to type into the chat
                input_text = "Hello, ChatGPT!"

                # Create a new instance of the web driver (e.g., Chrome)
                driver = webdriver.Chrome(executable_path=driver_path)

                # Open the website
                driver.get(website_url)

                # Wait for some time to let the page load
                time.sleep(5)

                # Find the chat input element by its HTML attribute (inspect the webpage to get the appropriate selector)
                input_element = driver.find_element_by_css_selector('input[type="text"]')

                # Type the input_text into the chat
                input_element.send_keys(input_text)

                # Press the Enter key to send the message
                input_element.send_keys(Keys.RETURN)

                # Wait for a few seconds to see the result
                time.sleep(3)

                # Close the browser
                driver.quit()

