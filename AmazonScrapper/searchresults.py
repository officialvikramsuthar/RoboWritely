import os

import jsonlines
from selectorlib import Extractor
import requests 
import json 
from time import sleep

BASE_PATH = os.path.dirname(__file__)
# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file(BASE_PATH + '/search_results.yml')

def scrape(url):  

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '25',
        'Content-Type': 'application/json',
        'Cookie': '_ga=GA1.1.431629955.1700216595; csrftoken=9vYO3gNshcWdaDgp8S0CIAqONtTpmjXzR6dEechkALi9QPFCI4UMWWST59u12n08; sessionid=q8iuf9bq1p8jdfbkf1yfal7dahy7jtim; _ga_7F29Q8ZGH0=GS1.1.1702450996.46.1.1702451993.59.0.0',
        'Key': '6d1409fc728c7cb105e1f28d9fcd44fa52b113cc',
        'Referer': 'https://www.amazon.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'x-csrftoken': '9vYO3gNshcWdaDgp8S0CIAqONtTpmjXzR6dEechkALi9QPFCI4UMWWST59u12n08'

    }



    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    return e.extract(r.text)


def scrap_search_results():

    url_data =  '''
        [{
  "Keyword": "Best 1TB SSD FOR PC",
  "URL": "https://www.amazon.com/s?k=wd+1+tb+ssd&i=computers&rh=n%3A1292116011%2Cp_n_feature_three_browse-bin%3A6797521011%2Cp_n_feature_twenty-five_browse-bin%3A21558461011&s=review-count-rank&dc&crid=AJZSETGN43I3&qid=1703223687&rnid=21558459011&sprefix=wd+1+tb+ss%2Caps%2C340&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&ref=sr_nr_p_n_feature_twenty-five_browse-bin_3&ds=v1%3AtRQ46N%2FTJUzUtPUGX3GiNfhHgSj3kJILljZPqUcsHic&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20&tag=refreshpage3-20"
},
{
  "Keyword": "Best 1TB SSD FOR Laptop (M.2)",
  "URL": "https://www.amazon.com/s?k=wd+1+tb+ssd+m.2&i=computers&rh=n%3A1292116011%2Cp_n_feature_three_browse-bin%3A6797521011%2Cp_n_feature_twenty-five_browse-bin%3A21558465011&s=review-rank&dc&qid=1703223865&rnid=21558459011&tag=refreshpage3-20%2Crefreshpage3-20%2Crefreshpage3-20%2Crefreshpage3-20&ref=sr_st_review-rank&ds=v1%3AHJTWGRbBh5nEI21DgEl3ODSyils%2FjqsYzNlBozu1T64"
}

    ]
    '''
    url_data = json.loads(url_data)
    # product_data = []
    products_urls = []
    # with open(BASE_PATH + "/search_results_urls.json",'r') as urllist, open(BASE_PATH + '/search_results_output.jsonl','w') as outfile:
    with open(BASE_PATH + '/search_results_output.jsonl','w') as outfile:
        import ipdb;ipdb.set_trace()
        for lines in url_data:
            url = lines.get('URL')
            keyword = lines.get('Keyword')

            if not url:
                continue

            data = scrape(url)

            if data and data.get('products'):
                product_list = []

                for product in data['products']:
                    reviews_count = product.get("reviews", "")
                    reviews_count = reviews_count.replace(",", "")

                    if int(reviews_count) > 1000:
                        prod_url = product.get("url", "")
                        products_urls.append(prod_url)
                        product['search_url'] = url
                        print("Saving Product: %s"%product['title'])
                        product_list.append(product)

                json.dump({keyword:product_list},outfile)
                outfile.write("\n")
                # sleep(5)

    with open(BASE_PATH + "/urls.txt", 'w') as urllist:
        for url in products_urls:
            urllist.write(url)
            urllist.write("\n")



