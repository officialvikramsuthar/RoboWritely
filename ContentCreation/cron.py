import os

from django_cron import CronJobBase, Schedule
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC


class GenerateContentCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'ContentCreation.GenerateContentCronJob'

    def do(self):

        BASE_DIR = os.path.dirname(os.path.realpath(__file__))
        DRIVER_PATH = os.path.realpath(os.path.join(BASE_DIR, '../chromedriver/chromedriver'))

        # URL of the website you want to visit (e.g., ChatGPT interface)
        HOME = os.path.expanduser('~')
        chrome_options = Options()
        chrome_options.add_argument("user-data-dir=/home/vikram/.config/google-chrome/Profile 1")
        service = ChromeService(executable_path=DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(r'https://www.google.co.in')
        time.sleep(5)
        driver.quit()



def chatgpt_code():
    driver.get(r'https://mail.google.com/mail/u/0/#inbox')

    loginBox = driver.find_element("xpath", '//*[@id="identifierId"]')
    loginBox.send_keys("vikram@trendlyne.com")

    nextButton = driver.find_element("xpath", '//*[@id="identifierNext"]/div/button')
    nextButton.click()
    time.sleep(3)

    passWordBox = driver.find_element("xpath", '//*[@id ="password"]/div[1]/div / div[1]/input')
    passWordBox.send_keys("V!kr@m9890")

    nextButton = driver.find_element("xpath", '//*[@id ="passwordNext"]')
    nextButton.click()

    time.sleep(10)

    driver.get("https://chat.openai.com/auth/login")
    time.sleep(5)

    nextButton = driver.find_element("xpath", '//*[@id="__next"]/div[1]/div[2]/div[1]/div/button[1]')
    nextButton.click()
    time.sleep(8)

    nextButton = driver.find_element("xpath", "/html/body/div/main/section/div/div/div/div[4]/form[2]/button")
    nextButton.click()
    time.sleep(8)

    nextButton = driver.find_element("xpath",
                                     '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[1]/div')
    nextButton.click()
    time.sleep(15)

    try:
        nextButton = driver.find_element("xpath",
                                         '//*[@id="radix-:ri:"]/div[2]/div/div[4]/button')
        nextButton.click()

    except Exception as e:
        print(e)

    prompt = "Write a blog of 4000 words about 'Indian Ancient History' in a heading and paragraph format"

    passWordBox = driver.find_element("xpath", '//*[@id="prompt-textarea"]')
    passWordBox.send_keys(prompt)
    time.sleep(10)
    nextButton = driver.find_element("xpath",
                                     '//*[@id="__next"]/div[1]/div[2]/div/main/div/div[2]/form/div/div[2]/button')
    nextButton.click()

    time.sleep(45)
    content = driver.find_element("xpath",
                                  '//*[@id="__next"]/div[1]/div/div/main/div/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/div').text
    print(content)
    time.sleep(5)

    nextButton = driver.find_element("xpath",
                                     '//*[@id="__next"]/div[1]/div[2]/div/main/div/div[1]/div/div/div/div[1]/div/div[2]/div[2]/button')

    nextButton.click()

    prompt = "Write a blog of 4000 words about 'indian history of 19th August' in a heading and paragraph format"
    passWordBox = driver.find_element("xpath", '//*[@id="prompt-textarea"]')
    passWordBox.send_keys(prompt)
    time.sleep(15)

    nextButton = driver.find_element("xpath",
                                     '//*[@id="__next"]/div[1]/div[2]/div/main/div/div[2]/form/div/div[2]/button')
    nextButton.click()
