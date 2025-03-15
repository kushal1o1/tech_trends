from django.contrib import admin
from .models import SubscribedCategory, Subscribers 
# Register your models here.
admin.site.register(SubscribedCategory)
admin.site.register(Subscribers)