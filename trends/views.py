from rest_framework import viewsets
from .models import TechNews
from .serializers import TechNewsSerializer

class TechNewsViewSet(viewsets.ModelViewSet):
    queryset = TechNews.objects.all()
    serializer_class = TechNewsSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset.order_by('?')
