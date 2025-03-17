from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Notification
from django.conf import settings
from .service import SendNotificationEmail

@receiver(post_save, sender=Notification)
def send_notification_to_all_users(sender, instance, created, **kwargs):
    if created:
        # Fetch all users
        SendNotificationEmail(instance)
        # users = Subscribers.objects.all()
        
        # # Send notification to each user (you can use any method: email, in-app, etc.)
        # for user in users:
            
        #     send_mail(
        #         'Notification',
        #         instance.message,
        #         settings.EMAIL_HOST_USER,
        #         [user.email],
        #         fail_silently=True
        #     )