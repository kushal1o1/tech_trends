from celery import shared_task
from .scraper import scrape_tech_news

@shared_task
def update_trends():
    scrape_tech_news()
    pass