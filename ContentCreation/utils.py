


import os
import shutil

class CreateGptBlog(object):

    def __init__(self, title):
        self.title = title
        self.heading_list = []
        self.headings = ""

    def get_intro_prompt(self):
        intro_prompt = f"""Disregard any prior instructions. Your responses should only be in English. Assume the role of a highly skilled SEO and top-tier copywriter who can fluently speak and write in English. Pretend that your English writing abilities are exceptional enough to surpass competing websites. Imagine that your content in English is of such high quality that it can outperform other sites. Refrain from stating that numerous factors affect search rankings. I am aware that content quality is just one aspect, and your mission is to create the best content possible, not to inform me about general SEO guidelines. Write and introduction of blog in 300 words for the title "{self.title}" where following are my headings - {self.headings} The Introduction should not contain the headings above. The response should be a paragraphs of approx 200-300 words. The response should be the text and not in a code format. The response should have appropriate HTML tags like <h3>, <li>, <p> so that it can be used in the Django template. It should not contain tags like <html><body><head> because it's not an html page but an HTML template that will be used. For every tag add classes as following for <h3> - blog-subsection-h3, <p> - blog-sub-section-para, <li> - blog-sub-section-list, <ul>- blog-sub-section-ul, <ol> - blog-subsection-ol. """

        return intro_prompt

    def get_heading_prompt(self):
        heading_prompt = f"""Disregard any prior instructions. Your responses should only be in English. Assume the role of a highly skilled SEO and top-tier copywriter who can fluently speak and write in English. Pretend that your English writing abilities are exceptional enough to surpass competing websites. Imagine that your content in English is of such high quality that it can outperform other sites. Refrain from stating that numerous factors affect search rankings. I am aware that content quality is just one aspect, and your mission is to create the best content possible, not to inform me about general SEO guidelines. I will provide the title "{self.title}" for an article that we aim to outshine on Google. Do not restate my request. Do not offer apologies. Refrain from self-referencing. Avoid generic filler language. Write an outline of a blog on "{self.title}" and nothing else should be there in response. It should be headings according to the the title. Headings should not include headings like "Introduction" and "Conclusion". There should not be any other extra information in the response."""

        return heading_prompt

    def set_heading(self, headings):

        for heading in headings.split("\n"):
            heading = heading.replace("<h2>", "")
            heading = heading.replace("</h2>", "")
            self.heading_list.append(heading)

        self.headings = "".join(self.heading_list)

    def get_heading_para_prompt(self, heading):
        heading_para_prompt = f"""Disregard any prior instructions. Your responses should only be in English. Assume the role of a highly skilled SEO and top-tier copywriter who can fluently speak and write in English. Pretend that your English writing abilities are exceptional enough to surpass competing websites. Imagine that your content in English is of such high quality that it can outperform other sites. Refrain from stating that numerous factors affect search rankings.  I am aware that content quality is just one aspect, and your mission is to create the best content possible, not to inform me about general SEO guidelines. Write a detailed informative article section where the heading "{heading}" of the blog I am writing with the title  "{self.title}". The response should only contain the information related to the heading and nothing else. The response should not contain the heading "{heading}". Add subheadings in the response. The response should have appropriate HTML tags like <h3>, <li>, <p> so that it can be used in the Django template. It should not contain tags like <html><body><head> because it's not an html page but an HTML template that will be used. For every tag add classes as following for <h3> - blog-subsection-h3, <p> - blog-sub-section-para, <li> - blog-sub-section-list, <ul>- blog-sub-section-ul, <ol> - blog-subsection-ol. """

        return heading_para_prompt

    def get_conclusion_prompt(self):
        conclusion_prompt = f"""Disregard any prior instructions. Your responses should only be in English. Assume the role of a highly skilled SEO and top-tier copywriter who can fluently speak and write in English. Pretend that your English writing abilities are exceptional enough to surpass competing websites. Imagine that your content in English is of such high quality that it can outperform other sites. Refrain from stating that numerous factors affect search rankings. I am aware that content quality is just one aspect, and your mission is to create the best content possible, not to inform me about general SEO guidelines. Write and conclusion of blog in 300 words for the title "{self.title}" where following are my headings - {self.headings} The conclusion should not contain the headings above. The response should be a paragraphs of approx 200-300 words. The response should have appropriate HTML tags like <h3>, <li>, <p> so that it can be used in the Django template. It should not contain tags like <html><body><head> because it's not an html page but an HTML template that will be used. For every tag add classes as following for <h3> - blog-subsection-h3, <p> - blog-sub-section-para, <li> - blog-sub-section-list, <ul>- blog-sub-section-ul, <ol> - blog-subsection-ol. """

        return conclusion_prompt

    def get_image_prompt(self, heading):
        image_prompt = f"""I am writing a blog about about {self.title} and one of the heading is {heading}, can you create an image which represents the heading {heading} correctly. The image should be copyright free and should not violate any rules for use."""

        return image_prompt

    def get_title_prompt(self):
        title_prompt = f"""Disregard any prior instructions. Your responses should only be in English. Assume the role of a highly skilled SEO and top-tier copywriter who can fluently speak and write in English. Pretend that your English writing abilities are exceptional enough to surpass competing websites. Imagine that your content in English is of such high quality that it can outperform other sites. Refrain from stating that numerous factors affect search rankings. I am aware that content quality is just one aspect, and your mission is to create the best content possible, not to inform me about general SEO guidelines. I will provide the title "{self.title}" for an article that we aim to outshine on Google. Do not restate my request. Do not offer apologies. Refrain from self-referencing. Avoid generic filler language. Give SEO friendly Title for the blog on "{self.title}". The response should contain the title only. No other information should be there in the response."""

        return title_prompt

    def get_meta_descriptions_prompt(self):
        meta_description_prompt = f"""Disregard any prior instructions. Your responses should only be in English. Assume the role of a highly skilled SEO and top-tier copywriter who can fluently speak and write in English. Pretend that your English writing abilities are exceptional enough to surpass competing websites. Imagine that your content in English is of such high quality that it can outperform other sites. Refrain from stating that numerous factors affect search rankings. I am aware that content quality is just one aspect, and your mission is to create the best content possible, not to inform me about general SEO guidelines. I will provide the title "{self.title}" for an article that we aim to outshine on Google. Do not restate my request. Do not offer apologies. Refrain from self-referencing. Avoid generic filler language. Give SEO friendly meta description for the blog on "{self.title}". The response should contain the meta description only. No other information should be there in the response."""

        return meta_description_prompt


class AudioBookPrompts(object):

    def get_context_prompt(self):
        intro_prompt = f"""Act as an expert in Hindi translation, Help me with Hindi translation. For Any given paragraph for translation, the translation will be in Devnagari script. For the words that does not have any hindi translation will be in Latin only. For example:
                          user:  "Welcome to the profound world of Stoicism, a philosophical school of thought that has shaped the minds and actions of countless individuals throughout history. Stoicism, much more than a mere philosophy, is a guide to a way of life - a compass to navigate the tumultuous seas of human existence."
                          response : "Stoicism के गहरे दुनिया में आपका स्वागत है, एक दार्शनिक विचार का जो इतिहास के दौरान अनगिनत व्यक्तियों के मस्तिष्क और क्रियाओं को आकार दिया है। Stoicism, केवल दर्शन नहीं, जीवन के एक तरीके का मार्गदर्शन है - मानव अस्तित्व के उतार-चढ़ावपूर्ण समुंदरों के संचलन के लिए एक कम्पास है।" 
                          I hope you got the context. for the future translations"""

        return intro_prompt

    def get_audio_book_prompt(self, title):
        prompt = f"""keeping the previous context can write short version of the panch tantra stories of "{title}" in Hindi in 600 Words. The response should contain the story and no other information. Don't apologize. Don't add acceptance. Do not add any extra information to the response."""

        return prompt

    def get_audio_book_prompt_english(self, title):
        prompt = f"""can you write the panch tantra story of "{title}".  Don't Add any other information in the response. The story should be suitable for children of the age up to 12 Years. The response should be 1000 words."""

        return prompt

def move_files(source_directory, destination_directory):
    # Check if the source directory exists
    if not os.path.exists(source_directory):
        print(f"Source directory '{source_directory}' does not exist.")
        return

    # Check if the destination directory exists, or create it if it doesn't
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Get a list of all files in the source directory
    files = os.listdir(source_directory)

    # Move each file from the source directory to the destination directory
    for file_name in files:
        source_path = os.path.join(source_directory, file_name)
        destination_path = os.path.join(destination_directory, file_name)
        shutil.move(source_path, destination_path)
        print(f"Moved '{file_name}' to '{destination_directory}'")
