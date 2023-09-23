


from django_cron import CronJobBase, Schedule
from ContentCreation.handler.chatgpt_selenium_automation import ChatGPTAutomation
import csv
import os
import platform

from ContentCreation.utils import CreateGptBlog


def create_file(filename, content):
    directory_name = "conversations"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    with open(os.path.join(directory_name, filename), "a") as file:
        file.write(content)


class GenerateContentCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'ContentCreation.GenerateContentCronJob'

    def do(self):
        import ipdb
        ipdb.set_trace()
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

                if len(lines) > 0 and index < 2:

                    try:
                        topic = "".join(lines)
                        obj = CreateGptBlog(topic)
                        blog = []

                        # Meta Description
                        meta_description_prompt = obj.get_title_prompt()
                        chatgpt.send_prompt_to_chatgpt(meta_description_prompt)
                        meta_description_response = chatgpt.return_last_response()
                        blog.append("<meta name='description' content='" + meta_description_response + "' />")

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
                        intro_prompt = obj.get_intro_prompt()
                        chatgpt.send_prompt_to_chatgpt(intro_prompt)
                        intro_response = chatgpt.return_last_response()
                        blog.append("<p class='blog-intro'>"+intro_response+"</p>")

                        # Loop Through all Headings
                        for heading in obj.heading_list:
                            blog.append("<h2 class='blog-sub-heading'>"+heading+"</h2>")
                            heading_prompt_para = obj.get_heading_para_prompt(heading)
                            chatgpt.send_prompt_to_chatgpt(heading_prompt_para)
                            heading_prompt_response = chatgpt.return_last_response()
                            heading_prompt_response = heading_prompt_response.replace(heading, "")
                            blog.append("<p class='blog-sub-heading-para'>"+heading_prompt_response+"</p>")

                        # Adding Conclusion
                        conlusion_prompt = obj.get_conclusion_prompt()
                        chatgpt.send_prompt_to_chatgpt(conlusion_prompt)
                        conlusion_response = chatgpt.return_last_response()
                        blog.append("<p class='conclusion-para'>"+conlusion_response+"</p>")

                        response = "".join(blog)
                        file_name = "{}.txt".format(topic)
                        create_file(file_name, response)

                    except Exception as e:
                        print(e)
                        chatgpt.star_new_chat()

            chatgpt.quit()