import requests
from bs4 import BeautifulSoup
from decouple import config
# from .models import TechNews

def scrape_tech_news():
    url = config('url')
    
    # Scrape Nepali Tech News
    nepali_tech_url = config('nepali_tech_url')
    nepali_tech_response = requests.get(nepali_tech_url)
    nepali_tech_soup = BeautifulSoup(nepali_tech_response.content, 'html.parser')
    nepali_tech_container = nepali_tech_soup.find('div', class_='newsTech_side-wrapper newsTech_side-min-lgflex')
    nepali_tech_articles = nepali_tech_container.find_all('li')
    
    for article in nepali_tech_articles:
        nepali_tech_title_tag = article.find('h4').find('a')
        nepali_tech_title = nepali_tech_title_tag.text
        nepali_tech_link = url + nepali_tech_title_tag['href']
        print(nepali_tech_title)
        # TechNews.objects.update_or_create(
        #     title=nepali_tech_title,
        #     link=nepali_tech_link,
        #     category='nepali'
        # )
        
    # Scrape Global Tech News
    global_tech_url = config('global_tech_url')
    global_tech_response = requests.get(global_tech_url)
    global_tech_soup = BeautifulSoup(global_tech_response.content, 'html.parser')
    global_tech_container = global_tech_soup.find('div', class_='newsTech_side-wrapper newsTech_side-min-lgflex')
    global_tech_articles = global_tech_container.find_all('li')
    
    for article in global_tech_articles:
        global_tech_title_tag = article.find('h4').find('a')
        global_tech_title = global_tech_title_tag.text
        global_tech_link = url + global_tech_title_tag['href']
        print(global_tech_title)
        # TechNews.objects.update_or_create(
        #     title=global_tech_title,
        #     link=global_tech_link,
        #     category='global'
        # )
scrape_tech_news()