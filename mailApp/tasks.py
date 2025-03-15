import logging
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from mailApp.models import Subscribers
import os
from django.core.mail import EmailMultiAlternatives
from django.template import Template, Context


@shared_task
def send_daily_email():
    logging.info("Starting the daily email task")
    print("Starting the daily email task")
    subscribers = Subscribers.objects.filter(SuscribeStatus=True)
    for subscriber in subscribers:
        subject = "Welcome to TechTrends!!"
             
        from_email = settings.EMAIL_HOST_USER
        to_list = [subscriber.email]
        # test
        context={
            "news":"Testing News"
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
        msg.failed_silently = True
        return True
        logging.info(f"Email sent to {subscriber.email}")
    logging.info("Finished the daily email task")
    return True
