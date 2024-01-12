import os
import time
from urllib.parse import urlparse, parse_qs, urlencode

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

from ContentCreation.handler.chatgpt_selenium_automation import ChatGPTAutomation
from PriceCompare.models import DiscPrice
from Robowritely.utils import get_chrome_path

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def replace_query_string(url, param_name, new_value):
    # Parse the URL
    parsed_url = urlparse(url)

    # Parse the query string into a dictionary
    query_dict = parse_qs(parsed_url.query)

    # Update the query string parameter with the new value
    query_dict[param_name] = [new_value]

    # Encode the updated query string
    updated_query_string = urlencode(query_dict, doseq=True)

    # Construct the new URL with the updated query string
    updated_url = parsed_url._replace(query=updated_query_string).geturl()

    return updated_url

def DiscPriceScrapping():
    chrome_path, chrome_driver_path = get_chrome_path(BASE_DIR)
    file_path = os.path.join(BASE_DIR, "output.jsonl")
    driver = ChatGPTAutomation(chrome_path, chrome_driver_path, url='https://diskprices.com/')

    time.sleep(3)
    response = driver.driver.page_source

    soup = BeautifulSoup(response, 'html.parser')

    table = soup.find('table')
    bulk_objs_ls = []
    field_header = ["price_per_gb","price_per_tb","price", "capacity", "warranty", "form_factor", "technology", "condition", "name"]
    for row in table.find_all('tr'):
        bulk_obj = DiscPrice()
        bulk_obj.country = "USA"
        print(len(row.find_all('td')))
        link = row.find('a')

        if link:
            link_href = link.get('href')
            try:
                link_href = replace_query_string(link_href, "tag", "officialvikra-20")
            except Exception as e:
                print(e)
            bulk_obj.Link = link_href
            for index, cell in enumerate(row.find_all('td')):
                print(cell.text, end='\t')
                print(index)
                if index < len(field_header):
                    print(field_header[index])
                    setattr(bulk_obj, field_header[index], cell.text)
            bulk_objs_ls.append(bulk_obj)
        print()

    created = DiscPrice.objects.bulk_create(bulk_objs_ls)
    print("objects created {}".format(created))
    driver.quit()

