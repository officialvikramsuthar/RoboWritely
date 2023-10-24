


from ContentCreation.utils import CreateGptBlog


class AmazonScrapperPrompats(CreateGptBlog):
    
    def get_intro_prompt(self):
        intro_prompt = f"""Disregard any prior instructions. Your responses should only be in English. Assume the role of a highly skilled SEO and top-tier copywriter who can fluently speak and write in English. Pretend that your English writing abilities are exceptional enough to surpass competing websites. Imagine that your content in English is of such high quality that it can outperform other sites. Refrain from stating that numerous factors affect search rankings. I am aware that content quality is just one aspect, and your mission is to create the best content possible, not to inform me about general SEO guidelines. Write and introduction of blog in 300 words for the title "{self.title}". The blog is product suggestion based on the customer reivew. The Introduction should not contain the headings above. The response should be a paragraphs of approx 200-300 words. The response should be the text and not in a code format. The response should have appropriate HTML tags like <h3>, <li>, <p> so that it can be used in the Django template. It should not contain tags like <html><body><head> because it's not an html page but an HTML template that will be used. For every tag add classes as following for <h3> - blog-subsection-h3, <p> - blog-sub-section-para, <li> - blog-sub-section-list, <ul>- blog-sub-section-ul, <ol> - blog-subsection-ol. """

        return intro_prompt
    
    def get_meta_descriptions_prompt(self):
        meta_description_prompt = f"""Disregard any prior instructions. Your responses should only be in English. Assume the role of a highly skilled SEO and top-tier copywriter who can fluently speak and write in English. Pretend that your English writing abilities are exceptional enough to surpass competing websites. Imagine that your content in English is of such high quality that it can outperform other sites. Refrain from stating that numerous factors affect search rankings. I am aware that content quality is just one aspect, and your mission is to create the best content possible, not to inform me about general SEO guidelines. I will provide the title "{self.title}" for an article that we aim to outshine on Google. Do not restate my request. Do not offer apologies. Refrain from self-referencing. Avoid generic filler language. Give SEO friendly meta description for the blog on "{self.title}". The response should contain the meta description only. No other information should be there in the response."""

        return meta_description_prompt

    def get_product_para(self, name, description, price):
        if not price:
            product_prompt = f"""name: {name}, description: {description}"""
        
        else:
            product_prompt = f"""name: {name}, description: {description} price: {price}"""

        return product_prompt 
    
    def get_product_prompt_initial_prompt(self):
        product_prompt = f"""Disregard any prior instructions. Your responses should only be in English. Assume the role of a highly skilled SEO and top-tier copywriter who can fluently speak and write in English. Pretend that your English writing abilities are exceptional enough to surpass competing websites. Imagine that your content in English is of such high quality that it can outperform other sites. Refrain from stating that numerous factors affect search rankings. I am aware that content quality is just one aspect, and your mission is to create the best content possible, not to inform me about general SEO guidelines. Do not restate my request. Do not offer apologies. Refrain from self-referencing. Avoid generic filler language. The response should have appropriate HTML tags like <h3>, <li>, <p> so that it can be used in the Django template. The response should contain the paragraph about product only. Don't add any other extra information in the  response which is not given in the description of the product. No other information should be there in the response. This prompt only for the for the framework. Don't add any heading for the product that have product name. I will you the name and details of the product in the following promot. Add a buying CTA by clicking on the button below which can support my work, but don't add the button html, that I will add it later. so don't answer to this prompt with any ambigous product details."""
        return product_prompt 
    


