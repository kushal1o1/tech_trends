import logging
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from mailApp.models import Subscribers
import os
from django.core.mail import EmailMultiAlternatives,get_connection
from django.template import Template, Context
from trends.models import TechNews
from .models import SubscribedCategory
from django.template.loader import render_to_string

def getNews(email):
    category_names = SubscribedCategory.objects.filter(
        subscribers__email=email
    ).values_list('name', flat=True)  # Get category names instead of IDs

    category_names = list(category_names)  # Convert QuerySet to list for safety

   
    if category_names:
        news_list = TechNews.objects.filter(category__in=category_names)  # Match category names
       
        
        return news_list
    else:
        print("No categories found for this subscriber.")
        return None

# @shared_task
# def send_daily_email():
#     logging.info("Starting the daily email task")
#     print("Starting the daily email task")
#     subscribers = Subscribers.objects.filter(SuscribeStatus=True)
#     for subscriber in subscribers:
       
#         subject = "Welcome to TechTrends!!"
             
#         from_email = settings.EMAIL_HOST_USER
#         to_list = [subscriber.email]
#         News=getNews(subscriber.email)
#         if not News:
#             print("NO news Found")
#             continue
        
#         # test
#         context={
#             "news":News
#         }
#         template_path = os.path.join(settings.BASE_DIR, "mailApp/templates/emails/TechTrendsNews.html")

#         # Read HTML content
#         with open(template_path, "r", encoding="utf-8") as f:
#             html_content = f.read()

#         django_template = Template(html_content)
#         rendered_html = django_template.render(Context(context))

#         # Send the email
#         msg = EmailMultiAlternatives(subject, "", from_email, to_list)
#         msg.attach_alternative(rendered_html, "text/html")
#         msg.send()
#         print("Mail Send to",to_list)
#         msg.failed_silently = True
#         return True
#     logging.info("Finished the daily email task")
#     return True
from celery import shared_task
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.conf import settings
import logging
import os

@shared_task
def send_daily_email():
    logging.info("Starting the daily email task")
    print("Starting the daily email task")

    subscribers = Subscribers.objects.filter(SuscribeStatus=True)
    if not subscribers:
        print("No subscribers found.")
        return False

    from_email = settings.EMAIL_HOST_USER
    subject = "Your Daily TechTrends Update!"
    
    # Create Email Connection (Allows Bulk Sending)
    connection = get_connection()

    email_messages = []  # Store all emails before sending

    for subscriber in subscribers:
        # Fetch Unique News for Each Subscriber
        news = getNews(subscriber.email)  
        if not news:
            print(f"No news found for {subscriber.email}")
            continue
        
        context = {"news": news}
        
        # Render HTML Content for Each User
        html_content = render_to_string("emails/TechTrendsNews.html", context)

        # Create Email
        msg = EmailMultiAlternatives(subject, "Here is your daily news update!", from_email, [subscriber.email], connection=connection)
        msg.attach_alternative(html_content, "text/html")

        # Add to Email List
        email_messages.append(msg)

    # Send All Emails in a Batch (Instead of One-by-One)
    if email_messages:
        connection.send_messages(email_messages)
        print(f"Sent {len(email_messages)} emails successfully.")
        logging.info(f"Sent {len(email_messages)} emails successfully.")
    else:
        print("No emails were sent.")
        logging.info("No emails were sent.")

    return True

