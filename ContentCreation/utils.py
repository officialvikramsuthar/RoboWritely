


class CreateGptBlog():

    def __init__(self, title):
        self.title = title
        self.heading_list = []
        self.headings = ""

    def get_intro_prompt(self):
        intro_prompt = f"""Disregard any prior instructions. 
                          Your responses should only be in English. 
                          Assume the role of a highly skilled SEO and top-tier copywriter who can fluently speak and write in English. 
                          Pretend that your English writing abilities are exceptional enough to surpass competing websites. 
                          Imagine that your content in English is of such high quality that it can outperform other sites. 
                          Refrain from stating that numerous factors affect search rankings. 
                          I am aware that content quality is just one aspect, and your mission is to create the best content possible, not to inform me about general SEO guidelines.
                          Write and introduction of blog in 300 words for the title "{self.title}" where following are my headings - 
                          {self.headings}
                          The Introduction should not contain the headings above. The response should be a paragraphs of approx 200-300 words."""

        return intro_prompt

    def get_heading_prompt(self):
        heading_prompt = f"""Disregard any prior instructions. Your responses should only be in English. 
                            Assume the role of a highly skilled SEO and top-tier copywriter who can fluently speak and write in English. 
                            Pretend that your English writing abilities are exceptional enough to surpass competing websites. 
                            Imagine that your content in English is of such high quality that it can outperform other sites. 
                            Refrain from stating that numerous factors affect search rankings. 
                            I am aware that content quality is just one aspect, and your mission is to create the best content possible, not to inform me about general SEO guidelines.
                            I will provide the title "{self.title}" for an article that we aim to outshine on Google. 
                            Do not restate my request. Do not offer apologies. 
                            Refrain from self-referencing. Avoid generic filler language. Write an outline of a blog on "{self.title}" and nothing else should be there in response. It should be 10 headings and headings should not include headings like "Introduction" and "Conclusion".
                            """

        return heading_prompt

    def set_heading(self, headings):
        self.heading = headings
        self.heading_list = headings.split(',')

    def get_heading_para_prompt(self, heading):
        heading_para_prompt = f"""Disregard any prior instructions. 
                                 Your responses should only be in English.
                                 Assume the role of a highly skilled SEO and top-tier copywriter who can fluently speak and write in English. 
                                 Pretend that your English writing abilities are exceptional enough to surpass competing websites. 
                                 Imagine that your content in English is of such high quality that it can outperform other sites. 
                                 Refrain from stating that numerous factors affect search rankings. 
                                 I am aware that content quality is just one aspect, and your mission is to create the best content possible, not to inform me about general SEO guidelines.
                                 Write a detailed informative article section where the heading "{heading}" of the blog I am writing with the title  "{self.title}". 
                                 The response should only contain the information related to the heading and nothing else. 
                                 The response should not contain the heading."""

        return heading_para_prompt

    def get_conclusion_prompt(self, heading):
        conclusion_prompt = f"""Disregard any prior instructions. 
                              Your responses should only be in English. 
                              Assume the role of a highly skilled SEO and top-tier copywriter who can fluently speak and write in English. 
                              Pretend that your English writing abilities are exceptional enough to surpass competing websites. 
                              Imagine that your content in English is of such high quality that it can outperform other sites. 
                              Refrain from stating that numerous factors affect search rankings. 
                              I am aware that content quality is just one aspect, and your mission is to create the best content possible, not to inform me about general SEO guidelines.
                              Write and conclusion of blog in 300 words for the title "{self.title}" where 
                              following are my headings - 
                               {self.headings}
                              The conclusion should not contain the headings above. The response should be a paragraphs of approx 200-300 words."""

        return conclusion_prompt

