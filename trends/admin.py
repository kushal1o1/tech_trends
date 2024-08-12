from django.contrib import admin
from .models import Trend

@admin.register(Trend)
class TrendAdmin(admin.ModelAdmin):
    list_display = ('title', 'timestamp', 'source_link')
    search_fields = ('title', 'description')
