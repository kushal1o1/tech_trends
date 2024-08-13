from rest_framework import viewsets
from .models import TechNews
from .serializers import TechNewsSerializer

class TechNewsViewSet(viewsets.ModelViewSet):
    queryset = TechNews.objects.all()
    serializer_class = TechNewsSerializer
