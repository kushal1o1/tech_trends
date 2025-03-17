import logging
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from mailApp.models import Subscribers
import os
from django.core.mail import EmailMultiAlternatives
from django.template import Template, Context
from trends.models import TechNews
from .models import SubscribedCategory

def getNews():
    category_names = SubscribedCategory.objects.filter(
        subscribers__email="kushalbaral101@gmail.com"
    ).values_list('name', flat=True)  # Get category names instead of IDs

    category_names = list(category_names)  # Convert QuerySet to list for safety

    print(f"Category Names: {category_names}")  # Debugging

    if category_names:
        news_list = TechNews.objects.filter(category__in=category_names)  # Match category names
        print(f"News found: {news_list}")  # Debugging
        
        return news_list
    else:
        print("No categories found for this subscriber.")
        return None

@shared_task
def send_daily_email():
    logging.info("Starting the daily email task")
    print("Starting the daily email task")
    subscribers = Subscribers.objects.filter(SuscribeStatus=True)
    for subscriber in subscribers:
        subject = "Welcome to TechTrends!!"
             
        from_email = settings.EMAIL_HOST_USER
        to_list = [subscriber.email]
        News=getNews()
        if not News:
            print("NO news Found")
            continue
        
        # test
        context={
            "news":News
        }
        template_path = os.path.join(settings.BASE_DIR, "mailApp/templates/emails/TechTrendsNews.html")

        # Read HTML content
        with open(template_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        django_template = Template(html_content)
        rendered_html = django_template.render(Context(context))

        # Send the email
        msg = EmailMultiAlternatives(subject, "", from_email, to_list)
        msg.attach_alternative(rendered_html, "text/html")
        msg.send()
        print("Mail Send")
        msg.failed_silently = True
        return True
    logging.info("Finished the daily email task")
    return True



