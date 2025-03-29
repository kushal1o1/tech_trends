import logging
import requests
from bs4 import BeautifulSoup
from decouple import config
from .models import TechNews
from ntscraper import Nitter
from django.db import transaction
# Fetch URLs from configuration
url = config('url')
nepali_tech_url = config('nepali_tech_url')
global_tech_url = config('global_tech_url')
tech_crunch_url = config('tech_crunch_url')
NEWS_API_KEY_NEWSAPIORG = config('NEWS_API_KEY_NEWSAPIORG')
    


def scrape_trending_news():
    with transaction.atomic():
                # TechNews.objects.filter(category='trending').delete()
                trending_tech_response = requests.get(nepali_tech_url)
                trending_tech_response.raise_for_status()
                trending_tech_soup = BeautifulSoup(trending_tech_response.content, 'html.parser')
                trending_tech_container = trending_tech_soup.find('div', class_='newsTech_side-wrapper newsTech_side-min-lgflex')
                trending_tech_articles = trending_tech_container.find_all('li')
                news_list = []
                for article in trending_tech_articles:
                    img_tag = article.find('img')
                    trending_tech_img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None   
                    trending_tech_title_tag = article.find('h4').find('a')
                    trending_tech_title = trending_tech_title_tag.text
                    trending_tech_title = trending_tech_title.strip()
                    trending_tech_link = url + trending_tech_title_tag['href']
                    news_list.append({
                        "title": trending_tech_title,
                        "link": trending_tech_link,
                        "image_url": trending_tech_img_url
                    })
                    # TechNews.objects.update_or_create(
                    #     title=trending_tech_title,
                    #     link=trending_tech_link,
                    #     category='trending',
                    #     img_url=trending_tech_img_url
                    # )
                with transaction.atomic():
                    TechNews.objects.filter(category='trending').delete()
                    TechNews.objects.bulk_create([
                        TechNews(title=news["title"], link=news["link"], category='trending', img_url=news["image_url"])
                        for news in news_list
                    ])
                return True

def scrape_nepali_tech_news():
    with transaction.atomic():
                # TechNews.objects.filter(category='nepali').delete()
                response = requests.get(nepali_tech_url)
                soup = BeautifulSoup(response.content, 'html.parser')
                divs = soup.find_all('div', class_='col-sm-6 col-md-4')
                news_list = []
                for div in divs:
                    title_tag = div.find('h4').find('a')
                    nepali_tech_title = title_tag.text.strip()
                    link = title_tag['href']
                    nepali_tech_link= url+link
                    img_tag = div.find('img')
                    nepali_tech_img_url = img_tag['src']
                    news_list.append({
                        "title": nepali_tech_title,
                        "link": nepali_tech_link,
                        "image_url": nepali_tech_img_url
                    })
                    # TechNews.objects.update_or_create(
                    #     title=nepali_tech_title,
                    #     link=nepali_tech_link,
                    #     category='nepali',
                    #     img_url=nepali_tech_img_url
                    # )
                with transaction.atomic():
                    TechNews.objects.filter(category='nepali').delete()
                    TechNews.objects.bulk_create([
                        TechNews(title=news["title"], link=news["link"], category='nepali', img_url=news["image_url"])
                        for news in news_list
                    ])
                return True
            
            
def scrape_global_tech_news():
    with transaction.atomic():
                # TechNews.objects.filter(category='global').delete()
                response = requests.get(global_tech_url)
                soup = BeautifulSoup(response.content, 'html.parser')
                divs = soup.find_all('div', class_='col-sm-6 col-md-4')
                news_list = []
                for div in divs:
                    title_tag = div.find('h4').find('a')
                    global_tech_title = title_tag.text.strip()
                    link = title_tag['href']
                    global_tech_link= url+link
                    img_tag = div.find('img')
                    global_tech_img_url = img_tag['src']
                    news_list.append({
                        "title": global_tech_title,
                        "link": global_tech_link,
                        "image_url": global_tech_img_url
                    })
                    # TechNews.objects.update_or_create(
                    #     title=global_tech_title,
                    #     link=global_tech_link,
                    #     category='global',
                    #     img_url=global_tech_img_url
                    # )
                with transaction.atomic():
                        TechNews.objects.filter(category='global').delete()
                        TechNews.objects.bulk_create([
                            TechNews(title=news["title"], link=news["link"], category='global', img_url=news["image_url"])
                            for news in news_list
                        ])
                return True
            
def scrape_ronb_news():
    with transaction.atomic():
                # TechNews.objects.filter(category='ronb').delete()
                scraper= Nitter()
                tweets =scraper.get_tweets('RONBupdates',mode='user',number=7)
                news_list = []
                for tweet in tweets['tweets']:
                    # ronb_title= tweet['text']
                    # ronb_img_url = tweet['pictures'][0] if tweet['pictures'] else None
                    # ronb_link= tweet['link']
                    news_list.append({
                    "title": tweet['text'],
                    "link": tweet['link'],
                    "image_url":  tweet['pictures'][0] if tweet['pictures'] else None
                    })
                    # TechNews.objects.update_or_create(
                    #     title=ronb_title,
                    #     link=ronb_link,
                    #     category='ronb',
                    #     img_url=ronb_img_url
                    # )
                with transaction.atomic():
                    TechNews.objects.filter(category='ronb').delete()
                    TechNews.objects.bulk_create([
                        TechNews(title=news["title"], link=news["link"], category='ronb', img_url=news["image_url"])
                        for news in news_list
                    ])
                return True
            
    
def scrape_news_api_org():
    TechNews.objects.filter(category='newsapinewsapiorg').delete()
    response = requests.get(f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={NEWS_API_KEY_NEWSAPIORG}")
    data = response.json()
    news_list = []
    if data["status"] == "ok":
        print("ok fetch")
        for article in data["articles"]:
            news_list.append({
            "title": (article["title"]),
            "link":(article["url"]),
            "image_url": article.get("urlToImage", "")
        })

        with transaction.atomic():
            TechNews.objects.filter(category='newsapinewsapiorg').delete()
            TechNews.objects.bulk_create([
                TechNews(title=news["title"], link=news["link"], category='newsapinewsapiorg', img_url=news["image_url"])
                for news in news_list
            ])
        return True
    else:
        False

def scrape_bbc_news():
    bbc_rss_url = config('bbc_url')
    response = requests.get(bbc_rss_url)
    
    if response.status_code != 200:
        print("Failed to fetch BBC Technology RSS Feed")
        return []
    
    soup = BeautifulSoup(response.content, "xml")
    articles = soup.find_all("item")  # RSS uses <item> for news entries
    
    news_list = []
    for article in articles[:10]:  # Get top 10 articles
        title = article.find("title").text if article.find("title") else "No Title"
        link = article.find("link").text if article.find("link") else "#"
        image = article.find("media:thumbnail")
        image_url = image["url"] if image else "No Image"
        
        news_list.append({
            "title": title,
            "link": link,
            "image_url": image_url
        })
    
    with transaction.atomic():
        TechNews.objects.filter(category='bbc').delete()
        TechNews.objects.bulk_create([
            TechNews(title=news["title"], link=news["link"], category='bbc', img_url=news["image_url"])
            for news in news_list
        ])
    
    return True
