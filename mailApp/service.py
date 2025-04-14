
import os
from django.core.mail import EmailMultiAlternatives
from tech_trends import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import  urlsafe_base64_encode
from django.utils.encoding import force_bytes 
from django.template import Template, Context
from .models import Subscribers


def SendConfirmEmail(verification_url,email,action="subscribe"):
    # Email Address Confirmation Email
        if action == "subscribe":
            from_email = settings.EMAIL_HOST_USER
            to_list = [email]
            template_path = os.path.join(settings.BASE_DIR, "mailApp/templates/emails/confirmEmail.html")
            email_subject = "Confirm for TechTrends Subscriptions"
            context ={ 
                "verification_link":verification_url
            }
            with open(template_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            django_template = Template(html_content)
            rendered_html = django_template.render(Context(context))
            # Send the email
            msg = EmailMultiAlternatives(email_subject, "", from_email, to_list)
            msg.attach_alternative(rendered_html, "text/html")
            msg.send()
            msg.failed_silently = True
            return True
        
        if action == "unsubscribe":
            from_email = settings.EMAIL_HOST_USER
            to_list = [email]
            template_path = os.path.join(settings.BASE_DIR, "mailApp/templates/emails/unsubscribe.html")
            email_subject = "Unsubscribe for TechTrends Subscriptions"
            context ={ 
                "verification_link":verification_url
            }
            with open(template_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            django_template = Template(html_content)
            rendered_html = django_template.render(Context(context))
            # Send the email
            msg = EmailMultiAlternatives(email_subject, "", from_email, to_list)
            msg.attach_alternative(rendered_html, "text/html")
            msg.send()
            msg.failed_silently = True
            return True
        
        if action =="update":
            print("sendingmail")
            from_email = settings.EMAIL_HOST_USER
            to_list = [email]
            template_path = os.path.join(settings.BASE_DIR, "mailApp/templates/emails/update_categories.html")
            email_subject = "Update Categories for TechTrends Subscriptions"
            context ={ 
                "verification_link":verification_url
            }
            with open(template_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            django_template = Template(html_content)
            rendered_html = django_template.render(Context(context))
            # Send the email
            msg = EmailMultiAlternatives(email_subject, "", from_email, to_list)
            msg.attach_alternative(rendered_html, "text/html")
            msg.send()
            print("mail send")
            msg.failed_silently = True
            return True


    
def SendNotificationEmail(instance):
    # Email Address Confirmation Email
        users = Subscribers.objects.all()
        from_email = settings.EMAIL_HOST_USER
        template_path = os.path.join(settings.BASE_DIR, "mailApp/templates/emails/notification.html")
        email_subject = "Notification Alert !!"
        context ={ 
            "message":instance.message
        }
        with open(template_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        django_template = Template(html_content)
        rendered_html = django_template.render(Context(context))

        # Send the email
       
        for user in users:
            msg = EmailMultiAlternatives(email_subject, "", from_email,[user.email])
            msg.attach_alternative(rendered_html, "text/html")
            msg.send()
            msg.failed_silently = True
        return True
    
