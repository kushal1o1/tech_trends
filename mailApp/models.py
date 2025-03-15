from django.db import models
CATEGORY_CHOICES = [
        ('nepali', 'Nepali Tech News'),
        ('global', 'Global Tech News'),
        ('trending', 'Trending  News'),
        ('ronb','Routine Of Nepal Banda')
        
    ]
# Create your models here.

class SubscribedCategory(models.Model):
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)
    def __str__(self):
        return self.category
class Subscribers(models.Model):
    email = models.EmailField()
    category =models.ManyToManyField(SubscribedCategory,related_name='subscribers')
    SuscribeStatus = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email
