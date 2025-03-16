from .models import  Subscribers,SubscribedCategory
from rest_framework import serializers
from rest_framework.response import Response
class subscribedCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribedCategory
        fields = ['id','name']
        
class SubscribersSerializer(serializers.ModelSerializer):
    category = subscribedCategorySerializer(many=True)

    class Meta:
        model = Subscribers
        fields = ['email', 'category', 'SuscribeStatus']

    