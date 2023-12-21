import requests
from bs4 import BeautifulSoup
import csv


# Function to scrape URLs from a page
def scrape_urls(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Replace 'your_class_name' with the actual class name of the <p> tags containing the URLs
        url_paragraphs = soup.find_all('p', class_='name')

        # Extract the URLs from the <p> tags
        urls = [paragraph.a['href'] for paragraph in url_paragraphs if paragraph.a]

        return urls
    else:
        print(f'Error: Unable to fetch URLs from {url}. Status code {response.status_code}')
        return []


# Function to save URLs to a CSV file
def save_urls_to_csv(urls):
    with open('scraped_urls.csv', 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['URL']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write the data rows
        for url in urls:
            writer.writerow({'URL': url})

    print('Scraping and saving URLs successful!')


# Replace 'your_website_url' with the actual URL of the website you want to scrape
# Replace 'your_class_name' with the actual class name of the <p> tags containing the URLs
website_url = 'https://concreteplayground.com/melbourne/bars'

# Scrape URLs from the page
page_urls = []
page_urls = scrape_urls(website_url)

for i in range(2, 25):
    pages = scrape_urls(website_url+'?paged={}'.format(i))
    page_urls = page_urls + pages


# Save URLs to a CSV file
save_urls_to_csv(page_urls)
