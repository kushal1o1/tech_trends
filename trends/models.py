from django.db import models
CATEGORY_CHOICES = [
        ('nepali', 'Nepali Tech News'),
        ('global', 'Global Tech News'),
        ('trending', 'Trending  News'),
        ('ronb','Routine Of Nepal Banda')
        
    ]
class TechNews(models.Model):
    
    
    title = models.CharField(max_length=255)
    link = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    img_url= models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.title


