from django.contrib import admin
from .models import SubscribedCategory, Subscribers,VerificationToken ,Notification
# Register your models here.
admin.site.register(SubscribedCategory)
admin.site.register(Subscribers)
admin.site.register(VerificationToken)
admin.site.register(Notification)
