from django.contrib import admin
from .models import TechNews
from django.utils.html import format_html

@admin.register(TechNews)
class TechNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'category', 'display_image')
    search_fields = ['category']
    def display_image(self, obj):
        if obj.img_url:
            return format_html('<img src="{}"alt="Img Not Found" width="100" height="100"/>', obj.img_url)
        return 'No Image'
    
    display_image.short_description = 'Image'