import requests
from bs4 import BeautifulSoup
import csv


# Function to scrape data from a single URL
def scrape_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Replace 'your_name_xpath', 'your_address_xpath', 'your_website_xpath' with the actual XPaths
        address = soup.find("div", class_="section-content").get_text() if soup.find("div", class_="section-content") else ''
        address = address.replace("\n", "")

        name = soup.find("h1", class_="title").get_text() if soup.find("h1", class_="title") else ''
        name = name.replace("\n", "")
        website = soup.find("section", class_="email places").a['href'] if soup.find("section", class_="email places") else ''
        date_created = soup.find("span", class_="created_at").get_text() if soup.find("span", class_="created_at") else ''
        date_created = date_created.replace("\n", "")

        style = soup.find("ul", class_="subinfo").get_text() if soup.find("ul", class_="subinfo") else ''
        style = style.replace("\n", "")

        area = soup.find("div", class_="section-content").a.get_text() if soup.find("div", class_="section-content").a else ''

        return {'Name': name, 'Address': address, 'Website': website, 'Area': area, 'Published_date':date_created, 'Style': style}
    else:
        print(f'Error: Unable to fetch data from {url}. Status code {response.status_code}')
        return {}


# Function to process URLs from a CSV file and save data to another CSV file
def process_urls(input_csv, output_csv):
    with open(input_csv, 'r', newline='', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        next(reader)  # Skip header row

        data_list = []

        for row in reader:
            url = row[0]

            # Scrape data from the current URL
            data = scrape_data(url)

            # Append the data to the list
            data_list.append(data)

    # Write all data to a new CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as output_file:
        fieldnames = ['Name', 'Address', 'Website', 'Area', 'Published_date', 'Style']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write the data rows
        for row in data_list:
            writer.writerow(row)

    print(f'Scraping and saving data successful. Results saved to {output_csv}')


# Replace 'your_name_xpath', 'your_address_xpath', 'your_website_xpath' with the actual XPaths
# Replace 'input_urls.csv' with the CSV file containing the URLs
# Replace 'output_data.csv' with the desired name for the output CSV file
process_urls('scraped_urls.csv', 'output_data.csv')
