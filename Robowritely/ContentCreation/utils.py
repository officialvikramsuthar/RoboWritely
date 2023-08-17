import openai

def generate_content_with_keywords(keywords):
    # Set up your OpenAI API key
    openai.api_key = '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'

    # Use the OpenAI API to generate content based on the provided keywords
    prompt = f""
    prompt = f"""
                Generate a blog of approx 500 words using the following keywords {keywords}. 
                the output should be return in json, where first key would be heading/title of the blog 
                and second key would be content of the blog. The content should be formatted in the HTML tags.
                for example the paragraphs should be in <p> tag and subheadings should be in <h2> tag. 
                if any other addition to improve the SEO is required that can be added too. 
                the content is not an html page, rather more like a component which will be added in the HTML page of django template
                hence everything in the content will be in the <div> tag
                """

    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
    )

    generated_content = response.choices[0].text.strip()

    # Split the generated content into headings and paragraphs
    sections = generated_content.split("\n")
    content_sections = [section.strip() for section in sections if section.strip()]

    # Create HTML content with headings and paragraphs
    heading = content_sections[0]  # First line is treated as the heading
    paragraphs = content_sections[1:]

    content_html = f"<h1>{heading}</h1>"
    for paragraph in paragraphs:
        # Treat lines starting with "#" as subheadings (you can adjust this logic)
        if paragraph.startswith("#"):
            content_html += f"<h2>{paragraph[1:].strip()}</h2>"
        else:
            content_html += f"<p>{paragraph}</p>"

    return {
        'heading': heading,
        'content': content_html,
    }
