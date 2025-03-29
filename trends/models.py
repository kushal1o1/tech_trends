from django.db import models
CATEGORY_CHOICES = [
        ('nepali', 'Nepali Tech News'),
        ('global', 'Global Tech News (Nepali)'),
        ('trending', 'Trending  News(Nepali)'),
        ('ronb','Routine Of Nepal Banda'),
        ('bbc','Tech BBC News'),
        ('newsapinewsapiorg','News API')
        
    ]
class TechNews(models.Model):
    
    
    title = models.CharField(max_length=255)
    link = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    img_url= models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.title


class NewsSources(models.Model):
    source_name = models.CharField(max_length=100, unique=True)
    source_url = models.URLField()
    source_image_link = models.URLField(blank=True, null=True)
    source_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.source_name