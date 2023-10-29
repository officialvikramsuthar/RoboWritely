


from django_cron import CronJobBase, Schedule
from AmazonScrapper.amazon import scrap_product_data
from AmazonScrapper.searchresults import scrap_search_results
import os
from AmazonScrapper.utils import AmazonScrapperPrompats
from ContentCreation.handler.chatgpt_selenium_automation import ChatGPTAutomation
from ContentCreation.utils import CreateGptBlog
from Robowritely.utils import clean_chat_gpt_response, create_file, get_chrome_path
import jsonlines
import json

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class ScrapSearchContentCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'ContentCreation.ScrapSearchContentCronJob'

    def do(self):
        scrap_search_results()


class ScrapProductContentCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'ContentCreation.ScrapSearchContentCronJob'

    def do(self):
        scrap_product_data()


class WriteAmazonBlog(CronJobBase):

    code = 'ContentCreation.WriteAmazonBlog'

    def do(self):
        chrome_path, chrome_driver_path = get_chrome_path(BASE_DIR)
        file_path = os.path.join(BASE_DIR, "output.jsonl")
        print(chrome_path)
        print(chrome_driver_path)
        chatgpt = ChatGPTAutomation(chrome_path, chrome_driver_path)
        
        # opening the CSV file
        with jsonlines.open(file_path, mode='r') as reader, open(BASE_DIR + '/search_results_output.jsonl','r') as search_results_output:

            chatgpt.star_new_chat()
            prompt_obj = AmazonScrapperPrompats("Best 10 vacuum cleaner cordless")
            blog = []

            # Meta Description
            meta_description_prompt = prompt_obj.get_meta_descriptions_prompt()
            chatgpt.send_prompt_to_chatgpt(meta_description_prompt)
            meta_description_response = chatgpt.return_last_response()
            clean_response = clean_chat_gpt_response(meta_description_response, ["Copy Code", "html"])
            blog.append("<meta>" + meta_description_response + "</meta>")

            # Title
            title_prompt = prompt_obj.get_title_prompt()
            chatgpt.send_prompt_to_chatgpt(title_prompt)
            title_response = chatgpt.return_last_response()
            clean_response = clean_chat_gpt_response(title_response, ["Copy Code", "html"], trim_comma=True)
            blog.append("<title>" + clean_response + "</title>")
            blog.append("<h1>"+clean_response+"</h1>")

             # Intro
            blog.append("<div class='blog-intro'>")
            intro_prompt = prompt_obj.get_intro_prompt()
            chatgpt.send_prompt_to_chatgpt(intro_prompt)
            intro_response = chatgpt.return_last_response()
            clean_response = clean_chat_gpt_response(intro_response, ["Copy Code", "html"])
            blog.append("<h2>Introduction</h2>")
            blog.append("<p class='blog-intro'>"+clean_response+"</p>")
            blog.append("</div>")

            products_inserted = 0
            for index, lines in enumerate(reader):

                if len(lines) <= 0:
                    continue

                if products_inserted == 10:
                    break

                try:
                    name=lines.get("name", "")
                    product_description = str(lines.get("product_description"))
                    short_description = str(lines.get("short_description", ""))
                    description = short_description + product_description
                    price = lines.get("price", "")
                    rating = lines.get("rating", "")
                    reviews = None
                    product_in_seach_result = None

                    for i in search_results_output:
                        if i.title == name:
                            product_in_seach_result = i
                            break

                    if product_in_seach_result and not price:
                        s_price = product_in_seach_result.get("price", 0)
                        price = s_price

                    if product_in_seach_result and not reviews:
                        s_rating = product_in_seach_result.get("reviews", "")
                        reviews = s_rating

                    if product_in_seach_result and not ratings:
                        s_ratinng = product_in_seach_result.get("rating", "")
                        rating = s_ratinng

                    if name and description and price:
                        product_prompt = prompt_obj.get_product_para(name,description, price, reviews, rating)
                        chatgpt.send_prompt_to_chatgpt(product_prompt)
                        product_response = chatgpt.return_last_response()
                        product_response = clean_chat_gpt_response(product_response, ["Copy Code", "html"])
                        blog.append("<div class='blog-subsection'>")
                        blog.append("<h2 class='blog-sub-heading'>"+name.strip('"')+"</h2>")
                        if lines.get("images", ""):
                            images = json.loads(lines.get("images", "")).keys()
                            src = ""
                            for index, key in enumerate(images):
                                if index == 1:
                                    src = key

                            blog.append(f"<div class='text-center'><img class='img-fluid my-5' src='{src}' alt='{name}' /></div>")
                        blog.append("<p class='blog-sub-heading-para'>"+product_response+"</p>")
                        href = lines.get("url", "")
                        if href:
                            blog.append(f"<div><a href='{href}'><button class='btn btn-dark px-3 rounded'><i class='bi bi-amazon'></i> Buy Now</button></a></div>")
                        else:
                            blog.append(f"<div><a href='amazon.com'><button class='btn btn-dark px-3 rounded'><i class='bi bi-amazon'></i> Buy Now</button></a></div>")

                        if ratings:
                            ratings_section = "<div class='ratings-section'>"
                            num_rating = float(ratings.replace("out of 5 stars", "").strip())
                            int_rating = int(num_rating)
                            fraction_rating = num_rating / int_rating

                            for i in range(0, int_rating):
                                ratings_section += "<i class='bi bi-star-fill rating-star-color'></i>"

                            if fraction_rating >= 0.5:
                                ratings_section += "<i class='bi bi-star-half rating-star-color'></i>"

                            ratings_section += f"{ratings}"

                            ratings_section += f"<br> <p class='public-reviews'> <i class='bi bi-person-lines-fill reviews-icon'></i> Reviews : {reviews}</p> </div>"

                        blog.append("</div>")

                        products_inserted += 1
                except Exception as e:
                    print(e)
                    chatgpt.star_new_chat()

            # Adding Conclusion
            blog.append("<div class='blog-conclusion'>")
            conlusion_prompt = prompt_obj.get_conclusion_prompt()
            chatgpt.send_prompt_to_chatgpt(conlusion_prompt)
            conlusion_response = chatgpt.return_last_response()
            clean_response = clean_chat_gpt_response(conlusion_response, ["Copy Code", "html"])
            # blog.append("<h2>Conclusion</h2>")
            blog.append("<p class='conclusion-para'>"+clean_response+"</p>")
            blog.append("</div>")

            response = "".join(blog)
            file_name = "{}.txt".format("Best 10 vacuum cleaner cordless")
            create_file(file_name, response)

            chatgpt.quit()
