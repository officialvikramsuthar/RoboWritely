


from django_cron import CronJobBase, Schedule
from AmazonScrapper.amazon import scrap_product_data
from AmazonScrapper.searchresults import scrap_search_results


class ScrapSearchContentCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'ContentCreation.ScrapSearchContentCronJob'

    def do(self):
        scrap_search_results()


class ScrapSearchContentCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'ContentCreation.ScrapSearchContentCronJob'

    def do(self):
        scrap_search_results()