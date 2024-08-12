from django.db import models

class Trend(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    source_link = models.URLField()  # Field for the source URL
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
