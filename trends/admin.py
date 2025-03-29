from django.contrib import admin
from .models import TechNews, NewsSources
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

admin.site.site_header = 'Tech News Admin'

@admin.register(NewsSources)
class NewsSourcesAdmin(admin.ModelAdmin):
    list_display = ('source_name', 'source_url', 'source_description','display_image')
    search_fields = ['source_name']
    list_filter = ['source_name']
    def display_image(self, obj):
        if obj.source_image_link:
            return format_html('<img src="{}"alt="Img Not Found" width="100" height="100"/>', obj.source_image_link)
        return 'No Image'
    display_image.short_description = 'Image'