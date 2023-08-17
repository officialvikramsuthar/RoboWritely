
from django_cron import CronJobBase, Schedule
from .models import Content
import csv
import openai

from .utils import generate_content_with_keywords


class GenerateContentCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'contentgenerator.generate_content_cron_job'

    def do(self):
        # Set up your OpenAI API key
        file_path =
        with open('.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                keywords = row[0]
                content = generate_content_with_keywords(keywords)
                Content.objects.create(keywords=keywords, content=content)
