import requests
import logging
from django.db import transaction
from service import delete_existing_records, scrape_tech_news, scrape_nepali_tech_news, scrape_global_tech_news, scrape_ronb_news

def scrape_tech_news():
    logging.info("Starting the tech news update task")
    # Clear existing records
    try:
        #  trending ones
            try:
                scrape_tech_news()
            except requests.RequestException as e:
                logging.error(f"Error fetching Trending  news: {e}")
            
            # Scrape Nepali Tech News
            try:
                scrape_nepali_tech_news()
            except requests.RequestException as e:
                logging.error(f"Error fetching Nepali tech news: {e}")

            # Scrape Global Tech News
            try:
               scrape_global_tech_news()
            except requests.RequestException as e:
                logging.error(f"Error fetching Global tech news: {e}")
            try:
                scrape_ronb_news()
            except Exception as e:
                logging.error(f"Error fetching Routine of Nepal Banda news: {e}")
            logging.info("Finished the tech news update task")
    except Exception as e:
        logging.error(f"Error updating tech news: {e}")
        raise e
    return True