from rest_framework import serializers
from .models import TechNews, NewsSources   

class TechNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechNews
        fields = '__all__'

class NewsSourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsSources
        fields = '__all__'

