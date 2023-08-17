# contentgenerator/cron.py

from django_cron import CronJobBase, Schedule
from .models import Content
import csv
import openai

class GenerateContentCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'contentgenerator.generate_content_cron_job'

    def do(self):
        # Set up your OpenAI API key
        openai.api_key = 'your-api-key'

        with open('your_keywords.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                keywords = row[0]
                content = self.generate_content_with_gpt(keywords)
                Content.objects.create(keywords=keywords, content=content)

    def generate_content_with_gpt(self, keywords):
        # Use the OpenAI API to generate content based on the provided keywords
        # Replace this with your actual ChatGPT code
        content = "Generated content based on " + keywords
        return content
