from django.contrib import admin
from .models import TechNews

@admin.register(TechNews)
class TechNewsAdmin(admin.ModelAdmin):
    list_display = ('title','link')
    search_fields = ['category']
