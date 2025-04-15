from django.db import models
from django.utils import timezone
import uuid
from trends.models import CATEGORY_CHOICES
CATEGORY_CHOICES = CATEGORY_CHOICES
# Create your models here.

class SubscribedCategory(models.Model):
    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)
    def __str__(self):
        return self.name
    
    
class Subscribers(models.Model):
    email = models.EmailField(unique=True)
    category =models.ManyToManyField(SubscribedCategory,related_name='subscribers')
    SuscribeStatus = models.BooleanField(default=False)
    verified=models.BooleanField(default=False)
    
    def __str__(self):
        return self.email
class VerificationToken(models.Model):
    email = models.EmailField(unique=True)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    verified = models.BooleanField(default=False)
    action=models.CharField(max_length=20, default="subscribe")
    data=models.JSONField(null=True, blank=True)  # Store additional data as JSON

    def __str__(self):
        return f"Verified:{self.verified}-{self.email}"
    

class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification: {self.message}"