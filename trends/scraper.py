import requests
import logging
from .service import scrape_trending_news, scrape_nepali_tech_news, scrape_global_tech_news, scrape_ronb_news, scrape_news_api_org,scrape_bbc_news,get_latest_hacker_news

def scrape_tech_news():
    logging.info("Starting the tech news update task")
    # Clear existing records
    try:
        #  trending ones
            try:
                if scrape_trending_news():
                    logging.info("Successfully fetched Trending news")
            except requests.RequestException as e:
                logging.error(f"Error fetching Trending  news: {e}")
            
            # Scrape Nepali Tech News
            try:
                if scrape_nepali_tech_news():
                    logging.info("Successfully fetched Nepali tech news")
            except requests.RequestException as e:
                logging.error(f"Error fetching Nepali tech news: {e}")

            # Scrape Global Tech News
            try:
               if scrape_global_tech_news():
                    logging.info("Successfully fetched Global tech news")
            except requests.RequestException as e:
                logging.error(f"Error fetching Global tech news: {e}")
            try:
                if scrape_ronb_news():
                    logging.info("Successfully fetched Routine of Nepal Banda news")
            except Exception as e:
                logging.error(f"Error fetching Routine of Nepal Banda news: {e}")
            try:
                if scrape_bbc_news():
                    logging.info("Successfully fetched BBC news")
            except Exception as e:
                logging.error(f"Error fetching BBC news: {e}")
            try:
                if scrape_news_api_org():
                    logging.info("Successfully fetched News API news")
            except Exception as e:
                logging.error(f"Error fetching News API news: {e}")
                
            # Scrape Hacker News
            try:
                if get_latest_hacker_news():
                    logging.info("Successfully fetched Hacker news")
            except requests.RequestException as e:
                logging.error(f"Error fetching Hacker news: {e}")
                
            logging.info("Finished the tech news update task")
    except Exception as e:
        logging.error(f"Error updating tech news: {e}")
        raise e
    return True