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


class GenerateContentCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'ContentCreation.GenerateContentCronJob'

    def do(self):
        # # Set up your OpenAI API key
        # file_path =
        # with open('.csv', 'r') as csv_file:
        #
        # Path to your WebDriver executable (e.g., chromedriver.exe)
        import ipdb
        ipdb.set_trace()
        BASE_DIR = os.path.dirname(os.path.realpath(__file__))
        DRIVER_PATH = os.path.realpath(os.path.join(BASE_DIR, '../chromedriver/chromedriver'))

        # URL of the website you want to visit (e.g., ChatGPT interface)
        website_url = 'https://chat.openai.com/'

        # Text you want to type into the chat
        input_text = "Hello, ChatGPT!"

        chrome_options = Options()
        chrome_options.add_argument("--disable-infobars")
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--disable-popup-blocking")
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument("--disable-application-cache")
        # chrome_options.add_argument('--disable-gpu')

        # Create a new instance of the web driver (e.g., Chrome)
        service = ChromeService(executable_path=DRIVER_PATH)
        browser = webdriver.Chrome(service=service, options=chrome_options)

        # Open the website
        browser.get(website_url)

        # Wait for some time to let the page load
        time.sleep(10)

        # Find the chat input element by its HTML attribute (inspect the webpage to get the appropriate selector)
        input_element = browser.find_element_by_css_selector('input[type="text"]')

        # Type the input_text into the chat
        input_element.send_keys(input_text)

        # Press the Enter key to send the message
        input_element.send_keys(Keys.RETURN)

        # Wait for a few seconds to see the result
        time.sleep(3)

        # Close the browser
        browser.quit()

