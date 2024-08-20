import requests
from bs4 import BeautifulSoup
from decouple import config
from .models import TechNews
import logging

def scrape_tech_news():
    logging.info("Starting the tech news update task")
    
    # Fetch URLs from configuration
    url = config('url')
    nepali_tech_url = config('nepali_tech_url')
    global_tech_url = config('global_tech_url')
    
    # Clear existing records
    TechNews.objects.filter(category='nepali').delete()
    TechNews.objects.filter(category='global').delete()
    TechNews.objects.filter(category='trending').delete()
    
    
#  trending ones
    try:
        trending_tech_response = requests.get(nepali_tech_url)
        trending_tech_response.raise_for_status()
        trending_tech_soup = BeautifulSoup(trending_tech_response.content, 'html.parser')
        trending_tech_container = trending_tech_soup.find('div', class_='newsTech_side-wrapper newsTech_side-min-lgflex')
        trending_tech_articles = trending_tech_container.find_all('li')
        
        for article in trending_tech_articles:
            img_tag = article.find('img')
            trending_tech_img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None   
            trending_tech_title_tag = article.find('h4').find('a')
            trending_tech_title = trending_tech_title_tag.text
            trending_tech_title = trending_tech_title.strip()
            trending_tech_link = url + trending_tech_title_tag['href']
            print(trending_tech_link)
            TechNews.objects.update_or_create(
                title=trending_tech_title,
                link=trending_tech_link,
                category='trending',
                img_url=trending_tech_img_url
            )
    except requests.RequestException as e:
        logging.error(f"Error fetching Trending  news: {e}")
    
    # Scrape Nepali Tech News
    try:
        response = requests.get(nepali_tech_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        divs = soup.find_all('div', class_='col-sm-6 col-md-4')
        for div in divs:
            title_tag = div.find('h4').find('a')
            nepali_tech_title = title_tag.text.strip()
            link = title_tag['href']
            nepali_tech_link= url+link
            img_tag = div.find('img')
            nepali_tech_img_url = img_tag['src']
            TechNews.objects.update_or_create(
                title=nepali_tech_title,
                link=nepali_tech_link,
                category='nepali',
                img_url=nepali_tech_img_url
            )
    except requests.RequestException as e:
        logging.error(f"Error fetching Nepali tech news: {e}")

    # Scrape Global Tech News
    try:
        response = requests.get(global_tech_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        divs = soup.find_all('div', class_='col-sm-6 col-md-4')
        for div in divs:
            title_tag = div.find('h4').find('a')
            global_tech_title = title_tag.text.strip()
            link = title_tag['href']
            global_tech_link= url+link
            img_tag = div.find('img')
            global_tech_img_url = img_tag['src']
            TechNews.objects.update_or_create(
                title=global_tech_title,
                link=global_tech_link,
                category='global',
                img_url=global_tech_img_url
            )
    except requests.RequestException as e:
        logging.error(f"Error fetching Global tech news: {e}")

    logging.info("Finished the tech news update task")
    print('DONE KUSHAL')
